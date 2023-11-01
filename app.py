from flask import Flask, request, jsonify, send_file, make_response, render_template
import csv
import psutil
from linkedin_api import linkedin, Linkedin
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from summarize import summarize
from translateenfr import translate_en_fr
from translatefren import translate_fr_en
from sentiment_analysis import sentiment_analysis
import re
import io
from flask_cors import CORS

from generate_report import generate_report_pdf

# Set the webdriver properties and options
driver_path = "geckodriver.exe"
firefox_binary = "C:\\Users\\abirb\\AppData\\Local\\Mozilla Firefox\\firefox.exe"


CLIENT_ID = '78dt2jx82cxwqy'
CLIENT_SECRET = 'faYLIU5bWMNs2Bbl'
REDIRECT_URI = 'http://127.0.0.1:5000/'




authentication = linkedin.LinkedAuthentication(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
authentication.authorization_code = 'AQULAdA4Oh_scLJ49MqlS6X_GU_Egsh2i-wO64m1SajJ6J_mqUZ8SJVU8xwKSbUROXDgDeGIiAXim_PhAFAvgroL2vn5XEW-F30c7JvtQD1HamMsNHJgjjZKRyDmUYz2ni8rQYuUc13BcDnE8gmRYw0XZIylm0oCz1uILa94kWE2LF8tbgeLX6a7VYvVhk9RPXyvUrQ1FMVpaUFKcHHjQILoSBLc-CIGPSsp504QwpRQn7XSoCGLV4ux3k31Lw33OzTYaKgMdpZBkXSKsq3tyMT2s91_uSd2-gD-DHjgmqJYWhApxH3tcH7-2X5Dz9viNmvJl96k6N3p-akxr9S2B8rV5wTxUg'
result = authentication.get_access_token()



# Set the webdriver.gecko.driver property
webdriver.Firefox.driver = driver_path

try:
    api = Linkedin('abir@mail.com', 'password')
except:
  print("An exception occurred")
result =''

# Set Firefox options
options = webdriver.FirefoxOptions()
options.binary_location = firefox_binary
options.add_argument("--headless")

# Create a new Firefox driver
driver = webdriver.Firefox(options=options)
tags = []
# Create the Flask app
app = Flask(__name__)
CORS(app)


# Define the API route to process the LinkedIn post URL
@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # Get the LinkedIn post URL from the request JSON data
        url = request.json['url']
        driver.get(url)

        i = 0
        nReactions = 0
        nComments = 0

        # Get the paragraph text
        paragraph_element = driver.find_element(By.XPATH, "/html/body/main/section[1]/div/section[1]/article/div[3]/p")
        post = paragraph_element.text

        # Split paragraphs using tags as separators
        paragraphs = re.split(r'\s*\n\s*#', post)

        paragraph = paragraphs[0]
        print(paragraph)

        # Get the tags
        while True:
            i += 1
            thetag = "/html/body/main/section[1]/div/section[1]/article/div[3]/p/a[" + str(i) + "]"
            try:
                tag_element = driver.find_element(By.XPATH, thetag)
                tag_text = tag_element.text
                if "#" in tag_text:
                    tags.append(tag_text)
            except:
                break
        print(tags)
        # Get the number of reactions
        reactions_element = driver.find_element(By.XPATH,
                                                "/html/body/main/section[1]/div/section[1]/article/div[4]/a[1]/span")
        nReactions = int(reactions_element.text)

        print(nReactions)

        # Get the number of comments
        try:
            comments_text_element = driver.find_element(By.XPATH,
                                                        "/html/body/main/section[1]/div/section[1]/article/div[4]/a[2]")
            comments_text = comments_text_element.text

            if "comment" in comments_text:
                nComments = 1
            else:
                nComments = int(comments_text.split(" ")[0])
        except:
            nComments = 0

        print(nComments)

        translated_en = translate_fr_en(paragraph)
        print(translated_en)

        summary = summarize(translated_en)
        print(summary)
        se = sentiment_analysis(summary)

        translated_fr = translate_en_fr(summary)
        print(translated_fr)

        # Visualize the number of reactions and comments
        plt.figure(figsize=(6, 4))
        plt.bar(["Reactions", "Comments"], [nReactions, nComments])
        plt.xlabel('Metrics')
        plt.ylabel('Count')
        plt.title('Reactions and Comments')
        plt.tight_layout()
        plt.show()

        # Extract emotions and scores from the response
        emotions = [emotion['label'] for emotion in se[0]]
        emotion_scores = [emotion['score'] for emotion in se[0]]

        # Sort emotions and scores in descending order based on scores
        sorted_emotions, sorted_scores = zip(*sorted(zip(emotions, emotion_scores), key=lambda x: x[1], reverse=True))

        # Sentiment Analysis Visualization
        plt.figure(figsize=(10, 6))  # Adjust the figure size for better readability
        plt.bar(sorted_emotions, sorted_scores)
        plt.xlabel('Emotions')
        plt.ylabel('Scores')
        plt.title('Sentiment Analysis')
        plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better visibility
        plt.tight_layout()
        plt.show()

        process = psutil.Process()
        process.cpu_percent()
        process.memory_info().rss

        from generate_report import generate_report_pdf

        # Generate the report PDF
        pdf_content = generate_report_pdf(translated_fr, tags, nReactions, nComments, se)

        # Create a response with the PDF data
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve the frontend HTML file

@app.route('/recommend')
def index():
    return render_template('recommend.html')

@app.route('/recomend', methods=['POST'])
def recomend():
    profile_ids = [request.form['profile_id1'], request.form['profile_id2'], request.form['profile_id3']]
    target_skills = request.form['target_skills'].split( ',')

    application = linkedin.LinkedInApplication(token=result.access_token)
    skills_array = []
    for profile_id in profile_ids:
        skills = application.get_profile_skills(profile_id)
        skills_array.append(skills)


    best_match_profile = None
    best_match_count = 0
    for i, skills in enumerate(skills_array):
        match_count = len(set(target_skills) & set(skills))
        if match_count > best_match_count:
            best_match_count = match_count
            best_match_profile = profile_ids[i]

    return jsonify({'best_match_profile': best_match_profile, 'target_skills': target_skills})


@app.route('/')
def serve_index():
    return send_file('index.html')

# Route to serve any static files (e.g., CSS, JS)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_file(f'static/{path}')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

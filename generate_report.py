from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import matplotlib.pyplot as plt
def generate_report_pdf(paragraph, tags, nReactions, nComments, sentiment_analysis):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
  # Define the styles for the PDF
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style = styles['Heading1']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Add the summary of the post to the PDF
    elements.append(Paragraph("Summary of the Post:", heading_style))
    elements.append(Paragraph(paragraph, normal_style))
    elements.append(Spacer(1, 12))

    # Add the tags to the PDF
    elements.append(Paragraph("Tags:", heading_style))
    tags_str = ", ".join(tags)
    elements.append(Paragraph(tags_str, normal_style))
    elements.append(Spacer(1, 12))

    # Add the number of reactions and comments to the PDF
    elements.append(Paragraph("Number of Reactions: {}".format(nReactions), heading_style))
    elements.append(Paragraph("Number of Comments: {}".format(nComments), heading_style))
    elements.append(Spacer(1, 12))

    # Visualize the number of reactions and comments
    plt.figure(figsize=(6, 4))
    plt.bar(["Reactions", "Comments"], [nReactions, nComments])
    plt.xlabel('Metrics')
    plt.ylabel('Count')
    plt.title('Reactions and Comments')
    plt.tight_layout()

    # Save the reactions and comments plot to a BytesIO buffer
    reactions_comments_buffer = BytesIO()
    plt.savefig(reactions_comments_buffer, format='png')
    plt.close()
    reactions_comments_buffer.seek(0)

    # Add the reactions and comments plot to the PDF
    reactions_comments_image = Image(reactions_comments_buffer, width=400, height=300)
    elements.append(Paragraph("Reactions and Comments Visualization:", heading_style))
    elements.append(reactions_comments_image)
    elements.append(Spacer(1, 12))


    # Add the sentiment analysis visualization to the PDF
    emotions = [emotion['label'] for emotion in sentiment_analysis[0]]
    emotion_scores = [emotion['score'] for emotion in sentiment_analysis[0]]

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

    # Save the sentiment analysis plot to a BytesIO buffer
    sentiment_buffer = BytesIO()
    plt.savefig(sentiment_buffer, format='png')
    plt.close()
    sentiment_buffer.seek(0)

    # Add the sentiment analysis plot to the PDF
    sentiment_image = Image(sentiment_buffer, width=400, height=300)
    elements.append(Paragraph("Sentiment Analysis Visualization:", heading_style))
    elements.append(sentiment_image)
    elements.append(Spacer(1, 12))

    # Build the PDF document with all the elements
    doc.build(elements, onFirstPage=generate_header_footer, onLaterPages=generate_header_footer)

    # Get the PDF content from the buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content

def generate_header_footer(canvas, doc):
    # Add header
    canvas.saveState()
    header_text = "Report for LinkedIn Post"
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawCentredString(300, 800, header_text)
    canvas.restoreState()

    # Add footer
    canvas.saveState()
    footer_text = "Page {} of {}".format(canvas.getPageNumber(), doc.page)
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(300, 30, footer_text)
    canvas.restoreState()

import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def summarize(paragraph):
    output = query({
        "inputs": paragraph,
    })



    return output[0]['summary_text']

# import requests
#
# API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr"
# headers = {"Authorization": "Bearer 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"}
#
#
# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()
#
#
#
#
# def translate_en_fr(paragraph):
#     output = query({
#         "inputs": paragraph,
#     })
#
#     translation_text = output[0]['translation_text']
#
#     return translation_text

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def translate_en_fr(english_text):
    tokenizer = AutoTokenizer.from_pretrained("model/opus-mt-en-fr")
    model = AutoModelForSeq2SeqLM.from_pretrained("model/opus-mt-en-fr")

    # Input English text

    # Tokenize the input text
    inputs = tokenizer.encode(english_text, return_tensors="pt")

    # Generate translation
    with torch.no_grad():
        translation_ids = model.generate(inputs)

    # Decode the generated translation
    translated_text = tokenizer.decode(translation_ids[0], skip_special_tokens=True)

    return translated_text



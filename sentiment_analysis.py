



from transformers import AutoTokenizer, RobertaForSequenceClassification
import torch


def sentiment_analysis(text):
    tokenizer = AutoTokenizer.from_pretrained("model/roberta-base-go_emotions")
    model = RobertaForSequenceClassification.from_pretrained("model/roberta-base-go_emotions")

    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    softmaxed_logits = torch.softmax(logits, dim=1)[0]
    scores = softmaxed_logits.tolist()

    emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"]

    results = [{'label': label, 'score': score} for label, score in zip(emotion_labels, scores)]

    sorted_results = [sorted(results, key=lambda x: x['score'], reverse=True)]

    return sorted_results



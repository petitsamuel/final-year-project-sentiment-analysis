from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline,
    CamembertTokenizer
)
from .text_processing import clean_texts_for_tf_model

# Init language classifier
tokenizer = AutoTokenizer.from_pretrained("moussaKam/barthez", add_special_tokens=True, do_lowercase=True, truncation=True, is_split_into_words=False)
model = AutoModelForSequenceClassification.from_pretrained("moussaKam/barthez-sentiment-classification")
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def predict_sentiment_barthez(texts):
    print("Analysis with Barthez model %d texts" % (len(texts)))
    cleaned_texts = clean_texts_for_tf_model(texts)
    print("Texts cleaned. Running classifier")
    output = []
    for t in cleaned_texts:
        result = classifier(t)[0]
        output.append(result)
        print("Predicted label: %s - Score %f" % (result['label'], result['score']))
    return output

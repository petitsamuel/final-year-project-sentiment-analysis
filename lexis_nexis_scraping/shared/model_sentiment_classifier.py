from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained(
    "tblard/tf-allocine", add_special_tokens=True, do_lowercase=True, truncation=True, is_split_into_words=False)
model = TFAutoModelForSequenceClassification.from_pretrained(
    "tblard/tf-allocine")

nlp = pipeline('sentiment-analysis', model=model,
               tokenizer=tokenizer, return_all_scores=True)


def compute_model_sentiment(texts):
    for i in range(len(texts)):
        texts[i] = texts[i][1]
    print(texts[0])
    print(nlp(texts[0]))

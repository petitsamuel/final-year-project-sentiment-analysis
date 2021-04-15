import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# This code did not end up being used. Uses the transformers library to
# perform sentiment classification on text from pre-trained models.
# Issue: The pipeline does not handle large text well & is mostly trained for short sized
# texts such as tweets etc.
# Using the `max_length=500, truncation=True` flags did not seem to fix.

barthez_tokenizer = AutoTokenizer.from_pretrained("moussaKam/barthez")
barthez_model = AutoModelForSequenceClassification.from_pretrained(
    "moussaKam/barthez-sentiment-classification")


def run_barthez_classifier(texts):
    print("Running Barthez Classifier")
    output = []
    for t in texts:
        input_ids = torch.tensor(
            # Encode tokenizes and maps to ids
            [barthez_tokenizer.encode(
                t[1], add_special_tokens=True, max_length=500, truncation=True)],
        )
        predict = barthez_model.forward(input_ids)[0]
        result = "positive" if predict.argmax(
            dim=-1).item() == 1 else "negative"
        output.append(result)
        print("Barthez Predicted %s" % (result))
    return output

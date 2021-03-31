import spacy

print("Loading spacy language package...")
nlp = spacy.load("fr_core_news_lg")
print("Done")

# camembert_tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
# camembert_tokenizer_fast = CamembertTokenizerFast.from_pretrained("camembert-base")

# def process_text_camembert():
#     tokenized_sentence = camembert_tokenizer.tokenize("Bonjour moi c'est samuel")
#     print(tokenized_sentence)


def process_text(text, remove_stop_words=True, vectorize=False):
    try:
        doc = nlp(text)
        if vectorize:
            return [token.vector_norm for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
        return [token.lemma_ for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
    except Exception as e:
        print(e)
        return []

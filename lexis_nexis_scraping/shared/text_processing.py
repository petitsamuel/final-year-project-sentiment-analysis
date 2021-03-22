import spacy

print("Loading spacy language package...")
nlp = spacy.load("fr_core_news_lg")
print("Done")


def process_text(text, remove_stop_words=True, vectorize=False):
    doc = nlp(text)
    if vectorize:
        return [token.vector_norm for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
    return [token.lemma_ for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]

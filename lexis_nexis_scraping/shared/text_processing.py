import spacy
from .models import punctuation

print("Loading spacy language package...")
nlp = spacy.load("fr_core_news_lg")
print("Loaded fr_core_news_lg")


def process_text(text, remove_stop_words=True, vectorize=False):
    try:
        doc = nlp(text)
        if vectorize:
            return [token.vector_norm for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
        return [token.lemma_ for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
    except Exception as e:
        print(e)
        return []


def lemmatize_lexicon(lexicon):
    doc = nlp(lexicon)
    return [token.lemma_ for token in doc if token.has_vector]


def tokenize_to_string_lemma(doc, truncate):
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.text.strip(
        punctuation)]
    if truncate and len(tokens) > 1024:
        tokens = tokens[:1024]
    return ' '.join(tokens)


def tokenize_to_string(doc, truncate):
    tokens = [token.text for token in doc if not token.is_stop and token.text.strip(
        punctuation)]
    if truncate and len(tokens) > 750:
        tokens = tokens[:750]
    return ' '.join(tokens)


def clean_text_for_analysis_lower(text, truncate=False):
    doc = nlp(text.lower())
    return tokenize_to_string_lemma(doc, truncate)


# Remove stop words and punctuations. Truncate tokens.
def clean_text_for_tf_model(text, truncate=True):
    doc = nlp(text)
    return tokenize_to_string(doc, truncate)


def clean_texts_for_tf_model(texts):
    print("Removing stop words, punctuation and truncating texts")
    output = []
    for t in texts:
        output.append(clean_text_for_tf_model(t[1]))
    return output

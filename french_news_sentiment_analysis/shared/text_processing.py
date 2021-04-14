import treetaggerwrapper as ttw
from treetaggerwrapper import Tag
import spacy
from .models import punctuation
from .folders import treetagger_path
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

print("Loading spacy language package...")
nlp = spacy.load("fr_core_news_lg")
print("Loaded fr_core_news_lg")

tagger = ttw.TreeTagger(TAGLANG='fr', TAGDIR=treetagger_path)


def process_text(text, remove_stop_words=True, vectorize=False):
    try:
        doc = nlp(text)
        if vectorize:
            return [token.vector_norm for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
        return [token.lemma_ for token in doc if (not remove_stop_words or not token.is_stop) and token.has_vector]
    except Exception as e:
        print(e)
        return []


def tokenize_to_string_lemma(doc, truncate=False):
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.text.strip(
        punctuation)]
    if truncate and len(tokens) > 1024:
        tokens = tokens[:1024]
    return ' '.join(tokens)


# Lowercase & remove stop words and punctuation from text.
def clean_text(text):
    return ' '.join([word for word in text.lower().split() if word not in fr_stop and word.strip(punctuation)])


def grab_lemmas_treetagger(clean_text):
    tags = tagger.tag_text(clean_text)
    lemmas = ttw.make_tags(tags)
    return ' '.join([v.lemma for v in lemmas if isinstance(v, Tag)])


def clean_text_for_analysis_lower(text, truncate=False):
    # Spacy Lemmatization approach
    doc = nlp(text.lower())
    return tokenize_to_string_lemma(doc, truncate)

    # TreeTagger Approach
    # cleaned_text = clean_text(text)
    # return grab_lemmas_treetagger(cleaned_text)

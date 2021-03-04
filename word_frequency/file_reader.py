import spacy
import re
import string

nlp = spacy.load('fr_core_news_sm')

def read_from_file(file_path, use_stemming = False):
    # read current file contents
    file = open(file_path, "r", encoding='utf-8', errors="ignore")
    contents = file.read().lower() # make all chars lowercase
    # replace all punctuaction
    for char in string.punctuation:
        contents = contents.replace(char, " ")
    # Remove all white space type chars (in any amount) to a single white space
    contents = re.sub('[\s]+', ' ', contents)
    if use_stemming == True:
        doc = nlp(contents)
        return [token.lemma_ for token in doc]
    # Split string into array of words (removes white spaces by default)
    return contents.split()

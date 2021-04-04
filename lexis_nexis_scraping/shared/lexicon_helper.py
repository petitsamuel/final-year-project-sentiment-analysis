from .folders import FEEL_lexicon, polarimots_lexicon
from .file_read_write import read_file
from .regex_helpers import count_intersections
from .models import FEELModel, FEELLexiconItem, PolarimotsItem
from .text_processing import clean_text_for_analysis_lower
import json


def load_feel_lexicon():
    data = read_file(FEEL_lexicon)
    lines = data.split("\n")[1:]  # skip first row
    del data
    output = {}
    for l in lines:
        if not l:
            continue
        values = l.split(";")
        output[values[FEELModel.word.index]] = FEELLexiconItem(*values)
    return output


def load_polarimots_lexicon(skip_neutral=True):
    data = read_file(polarimots_lexicon)
    lines = data.split("\n")
    del data
    output = {}
    for l in lines:
        if not l:
            continue
        values = l.split()
        model = PolarimotsItem(*values)
        if skip_neutral and model.polarity != 0:
            output[model.word] = model
    return output


def compute_sentiment(data, regexp, compute_output_from_counts):
    output = []
    for text in data:
        cleaned_text = clean_text_for_analysis_lower(text[1])
        counts = count_intersections(regexp, cleaned_text)
        output.append(compute_output_from_counts(counts))
    return output

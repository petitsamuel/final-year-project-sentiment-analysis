from .folders import FEEL_lexicon, polarimots_lexicon, diko_lexicon
from .file_read_write import read_file
from .regex_helpers import count_intersections
from .models import FEELModel, FEELLexiconItem, PolarimotsItem, DikoItem
from .text_processing import clean_text_for_analysis_lower
import numpy as np
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


def load_diko_lexicon(skip_neutral=True):
    print("Buidling Diko Lexicon")
    data = read_file(diko_lexicon)
    lines = data.split("\n")
    del data
    output = {}
    for l in lines[30:]:  # Lexicon starts line 30
        if not l:
            continue
        values = l.split(";")
        try:
            model = DikoItem(*values)
        except:
            # skip errors
            continue
        # if skip_neutral and model.polarity != 0:
        if model.get_vote_count() >= 500:
            output[model.word] = model
    stddev = np.std([x.get_vote_count() for x in output.values()])
    for x in output.values():
        x.compute_score(stddev)

    # Filter out somewhat neutral weights and entries with multiple words
    output = {k: v for k, v in output.items() if (v.weight <=
              -1 or v.weight >= 1) and len(v.word.split()) == 1}

    mean = np.mean([x.weight for x in output.values()])
    print("Mean of all weights for Diko Lexicon: %.4f" % (mean))
    return output


def compute_sentiment(data, regexp, compute_output_from_counts):
    output = []
    for text in data:
        cleaned_text = clean_text_for_analysis_lower(text[1])
        counts = count_intersections(regexp, cleaned_text)
        output.append(compute_output_from_counts(counts))
    return output

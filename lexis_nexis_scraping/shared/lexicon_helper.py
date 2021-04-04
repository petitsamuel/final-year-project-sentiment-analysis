from .folders import FEEL_lexicon, polarimots_lexicon
from .file_read_write import read_file
from .models import FEELModel, FEELLexiconItem, PolarimotsItem
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

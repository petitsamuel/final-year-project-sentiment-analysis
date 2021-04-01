from .folders import FEEL_lexicon
from .file_read_write import read_file
from .models import FEELModel, FEELLexiconItem
import json

def load_lexicon():
    data = read_file(FEEL_lexicon)
    lines = data.split("\n")[1:] # skip first row
    del data
    output = {}
    for l in lines:
        if not l:
            continue
        values = l.split(";")
        output[values[FEELModel.word.index]] = FEELLexiconItem(*values)
    return output

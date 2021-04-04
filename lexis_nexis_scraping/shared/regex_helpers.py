import re
from collections import Counter


# Escape all strings and wrap with \b (a regex word boundary)
def text_regex_mapper(s):
    return "\\b%s\\b" % (re.escape(s))


def compile_regex_from_lexicon(lexicon):
    words = lexicon.keys()
    return re.compile(r'%s' % '|'.join(
        map(text_regex_mapper, words)), flags=re.IGNORECASE)


def count_intersections(compiled_regex, text):
    output = []
    matches = compiled_regex.findall(text)
    return dict(Counter(matches))
    # Less efficient method
    # for x in lexicon_words:
    #     count = len(re.findall(r"\b" + re.escape(x) + r"\b", text))
    #     if count > 0:
    #         output.append([x, count])
    # return output

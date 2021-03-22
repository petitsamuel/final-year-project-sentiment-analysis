from shared.db_helpers import load_titles, init_db, load_full_articles
from collections import Counter
from shared.text_processing import process_text
from shared.variable_loader import write_to_file
from progress.bar import Bar
import json


def compute_frequencies(data):
    print("Loaded %d datapoints" % (len(data)))
    bar = Bar('Processing', max=len(data))
    counter = Counter()
    for text in data:
        cleaned = process_text(text[0])
        counter += Counter(cleaned)
        bar.next()
    print("\n")
    print(counter.most_common(50))
    total_words = sum(counter.values())
    return {'counter': counter, 'total_words': total_words}


def compute_title_freqs():
    init_db()
    data = load_titles()
    output = compute_frequencies(data)
    write_to_file(output, 'title_frequencies.json')
    print(output['total_words'])


def compute_articles_freqs():
    init_db()
    data = load_full_articles()
    output = compute_frequencies(data)
    write_to_file(output, 'articles_body_frequencies.json')
    print(output['total_words'])


compute_title_freqs()

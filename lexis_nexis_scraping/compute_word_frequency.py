from shared.db_helpers import load_titles, init_db, load_full_articles, load_titles_group_month, load_articles_group_month
from collections import Counter
from shared.text_processing import process_text
from shared.variable_loader import write_to_file
from shared.folders import articles_words_freq, titles_words_freq, title_monthly_frequencies, articles_monthly_frequencies
from progress.bar import Bar
import json
import string

punctuation = r'«»‹›' + string.punctuation


def get_key(m, y):
    # To be able to use json dumps, keys must be strings
    return str(m) + "_" + str(y)


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


def compute_frequencies_by_month(data):
    print("Loaded %d datapoints" % (len(data)))
    bar = Bar('Processing', max=len(data))
    data_dict = {}
    for text, month, year in data:
        if get_key(month, year) not in data_dict:
            data_dict[get_key(month, year)] = Counter()
        cleaned = process_text(text)
        data_dict[get_key(month, year)] += Counter(cleaned)
        bar.next()
    print("\nKeeping first 30 most common words for each month")
    for key in data_dict.keys():
        print("Processing %s" % (key))
        data_dict[key] = Counter(
            {k: v for k, v in data_dict[key].items() if k.strip(punctuation)})
        data_dict[key] = data_dict[key].most_common(30)
    return data_dict


def compute_title_freqs():
    init_db()
    data = load_titles()
    output = compute_frequencies(data)
    write_to_file(output, titles_words_freq)
    print(output['total_words'])


def compute_title_freqs_by_month():
    init_db()
    data = load_titles_group_month()
    output = compute_frequencies_by_month(data)
    write_to_file(output, title_monthly_frequencies)


def compute_articles_freqs_by_month():
    init_db()
    data = load_articles_group_month()
    output = compute_frequencies_by_month(data)
    write_to_file(output, articles_monthly_frequencies)


def compute_articles_freqs():
    init_db()
    data = load_full_articles()
    output = compute_frequencies(data)
    write_to_file(output, articles_words_freq)
    print(output['total_words'])


compute_articles_freqs_by_month()

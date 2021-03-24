from shared.db_helpers import load_titles, init_db, load_full_articles, load_titles_group_month, load_articles_group_month, load_titles_group_week, load_articles_group_week, load_word_counts_weekly
from collections import Counter
from shared.text_processing import process_text
from shared.variable_loader import write_to_file
from shared.folders import articles_words_freq, titles_words_freq, title_monthly_frequencies, articles_monthly_frequencies, title_weekly_frequencies, articles_weekly_frequencies, weekly_average_word_count
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
    print("\nKeeping first 10 most common words for each month & computing relative frequencies...")
    for key in data_dict.keys():
        print("Processing %s" % (key))
        # Get relative frequency & remove punctuation
        total_word_count = sum(data_dict[key].values())
        tmp_dict = {k: float(v)/float(total_word_count)
                    for k, v in data_dict[key].items() if k.strip(punctuation)}
        # keep last 10 elements (most frequent)
        data_dict[key] = dict(
            sorted(tmp_dict.items(), key=lambda item: item[1])[-10:])
    return data_dict


def compute_frequencies_by_week(data):
    print("Loaded %d datapoints" % (len(data)))
    bar = Bar('Processing', max=len(data))
    data_dict = {}
    for text, week in data:
        if week not in data_dict:
            data_dict[week] = Counter()
        cleaned = process_text(text)
        data_dict[week] += Counter(cleaned)
        bar.next()
    print("\nKeeping first 10 most common words for each week & computing relative frequencies...")
    for key in data_dict.keys():
        print("Processing %s" % (key))
        # Get relative frequency & remove punctuation
        total_word_count = sum(data_dict[key].values())
        tmp_dict = {k: float(v)/float(total_word_count)
                    for k, v in data_dict[key].items() if k.strip(punctuation)}
        # keep last 10 elements (most frequent)
        data_dict[key] = dict(
            sorted(tmp_dict.items(), key=lambda item: item[1])[-10:])
    return data_dict


def format_weekly_word_count(data):
    output = {}
    for word_sum, article_count, average, week in data:
        output[int(week)] = {
            'word_sum': int(word_sum),
            'article_count': int(article_count),
            'average_word_count': float(average)
        }
    return output


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


def compute_title_freqs_by_week():
    init_db()
    data = load_titles_group_week()
    output = compute_frequencies_by_week(data)
    write_to_file(output, title_weekly_frequencies)


def compute_articles_freqs_by_month():
    init_db()
    data = load_articles_group_month()
    output = compute_frequencies_by_month(data)
    write_to_file(output, articles_monthly_frequencies)


def compute_articles_freqs_by_week():
    init_db()
    data = load_articles_group_week()
    output = compute_frequencies_by_week(data)
    write_to_file(output, articles_weekly_frequencies)


def compute_average_word_count_weekly():
    init_db()
    data = load_word_counts_weekly()
    output = format_weekly_word_count(data)
    write_to_file(output, weekly_average_word_count)


def compute_articles_freqs():
    init_db()
    data = load_full_articles()
    output = compute_frequencies(data)
    write_to_file(output, articles_words_freq)
    print(output['total_words'])


# Compute list of most used words grouped monthly
# compute_title_freqs_by_month()
# compute_articles_freqs_by_month()

# Compute list of most used words grouped weekly
compute_title_freqs_by_week()
compute_articles_freqs_by_week()

# Compute average word count per articles grouped weekly
compute_average_word_count_weekly()

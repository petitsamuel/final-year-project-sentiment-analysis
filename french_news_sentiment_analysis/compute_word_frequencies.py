from shared.db_helpers import articles_by_month, titles_by_month, init_db, load_word_counts_weekly, fetch_script_from_db
from collections import Counter
from shared.text_processing import process_text
from shared.file_read_write import write_to_file
from shared.folders import title_monthly_frequencies, articles_monthly_frequencies, weekly_average_word_count, monthly_average_word_count
from progress.bar import Bar
import string

punctuation = r'«»‹›' + string.punctuation

# Loads data from the database, cleans articles (using lemmatization, stop word removal & lowercase)
# to generate json files (available in the data directory) with the following data:
# title word frequencies, article word frequencies, average word counts grouped weekly & monthly.


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


# def get_key(m, y):
#     # To be able to use json dumps, keys must be strings
#     return str(m) + "_" + str(y)
# def compute_frequencies_by_month(data):
#     print("Loaded %d datapoints" % (len(data)))
#     bar = Bar('Processing', max=len(data))
#     data_dict = {}
#     for text, month, year in data:
#         if get_key(month, year) not in data_dict:
#             data_dict[get_key(month, year)] = Counter()
#         cleaned = process_text(text)
#         data_dict[get_key(month, year)] += Counter(cleaned)
#         bar.next()
#     print("\nKeeping first 10 most common words for each month & computing relative frequencies...")
#     for key in data_dict.keys():
#         print("Processing %s" % (key))
#         # Get relative frequency & remove punctuation
#         total_word_count = sum(data_dict[key].values())
#         tmp_dict = {k: float(v)/float(total_word_count)
#                     for k, v in data_dict[key].items() if k.strip(punctuation)}
#         # keep last 10 elements (most frequent)
#         data_dict[key] = dict(
#             sorted(tmp_dict.items(), key=lambda item: item[1])[-10:])
#     return data_dict


# def compute_frequencies_by_week(data):
#     print("Loaded %d datapoints" % (len(data)))
#     bar = Bar('Processing', max=len(data))
#     data_dict = {}
#     for text, week in data:
#         if week not in data_dict:
#             data_dict[week] = Counter()
#         cleaned = process_text(text)
#         data_dict[week] += Counter(cleaned)
#         bar.next()
#     print("\nKeeping first 10 most common words for each week & computing relative frequencies...")
#     for key in data_dict.keys():
#         print("Processing %s" % (key))
#         # Get relative frequency & remove punctuation
#         total_word_count = sum(data_dict[key].values())
#         tmp_dict = {k: float(v)/float(total_word_count)
#                     for k, v in data_dict[key].items() if k.strip(punctuation)}
#         # keep last 10 elements (most frequent)
#         data_dict[key] = dict(
#             sorted(tmp_dict.items(), key=lambda item: item[1])[-10:])
#     return data_dict


def format_weekly_word_count(data):
    output = []
    for word_sum, article_count, average, week, year in data:
        output.append({
            'word_sum': int(word_sum),
            'article_count': int(article_count),
            'average_word_count': float(average),
            'week': week,
            'year': year
        })
    return output


def format_monthly_word_count(data):
    output = []
    for word_sum, article_count, average, month, year in data:
        output.append({
            'word_sum': int(word_sum),
            'article_count': int(article_count),
            'average_word_count': float(average),
            'month': month,
            'year': year
        })
    return output


def compute_articles_freqs_by_month():
    months_list = fetch_script_from_db('all_months_year.sql')
    computed_data = {}
    for month, year in months_list:
        print("Computing Month %d - Year %d" % (month, year))
        articles = articles_by_month(month, year, 3000)
        output = compute_frequencies(articles)
        computed_data["%d-%d" % (year, month)] = output

    write_to_file(computed_data, articles_monthly_frequencies)


def compute_title_freqs_by_month():
    months_list = fetch_script_from_db('all_months_year.sql')
    computed_data = {}
    for month, year in months_list:
        print("Computing Month %d - Year %d" % (month, year))
        titles = titles_by_month(month, year, 3000)
        output = compute_frequencies(titles)
        computed_data["%d-%d" % (year, month)] = output

    write_to_file(computed_data, title_monthly_frequencies)


def compute_average_word_count_monthly():
    data = fetch_script_from_db("monthly_word_counts.sql")
    output = format_monthly_word_count(data)
    write_to_file(output, monthly_average_word_count)


def compute_average_word_count_weekly():
    data = load_word_counts_weekly()
    output = format_weekly_word_count(data)
    write_to_file(output, weekly_average_word_count)


init_db()
# Compute list of most used words grouped monthly
compute_title_freqs_by_month()
compute_articles_freqs_by_month()

# Compute average word count per articles grouped weekly
compute_average_word_count_weekly()
compute_average_word_count_monthly()

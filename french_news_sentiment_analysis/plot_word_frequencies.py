from shared.file_read_write import read_file
from shared.dates_helper import date_from_month
from shared.folders import title_monthly_frequencies, articles_monthly_frequencies, titles_word_freq_wordcloud, articles_word_freq_wordcloud
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import string
import re
import json

punctuation = r'«»‹›' + string.punctuation


def make_date_map(str_dates):
    output = {}
    for d in str_dates:
        year, month = d.split("-")
        date = date_from_month(int(month),  int(year))
        output[d] = date
    return dict(sorted(output.items(), key=lambda item: item[1]))


def format_data(data, dates_map):
    # we got date -> all counts
    # map it to: word -> [counts...]
    output = {}
    index = 0
    for key, value in dates_map.items():
        data_at_date = data[key]['counter']
        total_word_count = data[key]['total_words']
        data_at_date = {k: float(v)/float(total_word_count)
                        for k, v in data_at_date.items() if k.strip(punctuation) and len(k) > 2}
        for word, count in data_at_date.items():
            if word not in output:
                output[word] = [0 for _ in range(len(dates_map))]
            output[word][index] = count
        index += 1

    return dict(sorted(output.items(), key=lambda item: sum(item[1]))[-15:])


def generate_monthly_plot(data, graph_name):
    dates_str = data.keys()
    dates_map = make_date_map(dates_str)

    formatted_data = format_data(data, dates_map)
    dates = list(dates_map.values())

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key, value in formatted_data.items():
        ax.plot(dates[1:], value[1:], label=key)
    ax.set_xlabel("Date")
    ax.set_ylabel("Relative Frequency")
    ax.set_yscale("log")
    ax.set_title(
        "Most Frequent Words in %s Monthly on a Logarithmic Scale" % (graph_name))
    ax.legend(loc='lower right')


def plot_word_cloud(data, graph_name, path):
    summed_counter = Counter()
    sum_words = 0
    for _, values in data.items():
        summed_counter += Counter(values['counter'])
        sum_words += values['total_words']
    if '\xa0' in summed_counter:
        del summed_counter['\xa0']

    frequencies = {k: float(v)/float(sum_words)
                   for k, v in summed_counter.items() if k.strip(punctuation) and len(k) > 2}

    wc = WordCloud(max_font_size=50, max_words=100,
                   background_color="white").generate_from_frequencies(frequencies)
    wc.to_file(path)
    print("Saved wordcloud of word frequencies for %s at file %s" %
          (graph_name, path))


def plot_titles_monthly():
    data = json.loads(read_file(title_monthly_frequencies))
    generate_monthly_plot(data, "Titles")
    plot_word_cloud(data, "Titles", titles_word_freq_wordcloud)


def plot_articles_monthly():
    data = json.loads(read_file(articles_monthly_frequencies))
    generate_monthly_plot(data, "Articles")
    plot_word_cloud(data, "Articles", articles_word_freq_wordcloud)


plot_articles_monthly()
plot_titles_monthly()

plt.show()

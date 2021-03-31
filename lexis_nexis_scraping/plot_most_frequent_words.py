from shared.file_read_write import read_file
from shared.dates_helper import date_from_month
from shared.folders import titles_words_freq, articles_words_freq, title_monthly_frequencies, articles_monthly_frequencies, weekly_average_word_count, title_weekly_frequencies, articles_weekly_frequencies
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
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
        data_at_date = {k: float(v)/float(total_word_count) for k, v in data_at_date.items() if k.strip(punctuation)}
        for word, count in data_at_date.items():
            if word not in output:
                output[word] = [0 for _ in range(len(dates_map))]
            output[word][index] = count
        index += 1

    return dict(sorted(output.items(), key=lambda item: sum(item[1]))[-15:])


def format_weekly_data(data):
    # we got date -> all counts
    # map it to: word -> [counts...]
    output = {}
    index = 0
    data_len = len(data.keys())
    for key in data.keys():
        data_at_date = data[key]
        for word, freq in data_at_date.items():
            if word not in output:
                output[word] = [0 for _ in range(data_len)]
            output[word][index] = freq
        index += 1
    return output


def generate_monthly_plot(data):
    dates_str = data.keys()
    dates_map = make_date_map(dates_str)

    formatted_data = format_data(data, dates_map)
    dates = dates_map.values()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key, value in formatted_data.items():
        ax.plot(dates, value, label=key)
    ax.set_xlabel("Date")
    ax.set_yscale('log')
    ax.set_title(
        "Most frequent word counts per month")
    ax.legend(loc='lower right')

def sum_counters(data):
    summed_counter = Counter()
    sum_words = 0
    for _, values in data.items():
        summed_counter += Counter(values['counter'])
        sum_words += values['total_words']
    if '\xa0' in summed_counter:
        del summed_counter['\xa0']

    frequencies = {k: float(v)/float(sum_words) for k, v in summed_counter.items() if k.strip(punctuation)}

    wc = WordCloud().generate_from_frequencies(frequencies)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

def plot_titles_monthly():
    data = json.loads(read_file(title_monthly_frequencies))
    generate_monthly_plot(data)
    sum_counters(data)


def plot_articles_monthly():
    data = json.loads(read_file(articles_monthly_frequencies))
    generate_monthly_plot(data)
    sum_counters(data)



def plot_word_cloud(file):
    data = json.loads(read_file(file))
    total_word_count = data['total_words']
    data = {k: float(v)/float(total_word_count) for k, v in data['counter'].items(
    ) if k.strip(punctuation)}
    if data == None:
        print("Error: file %s not found" % file)
        exit(1)
    wc = WordCloud().generate_from_frequencies(data)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")


# plot_word_cloud(titles_words_freq)
# plot_word_cloud(articles_words_freq)

plot_articles_monthly()
plot_titles_monthly()

plt.show()

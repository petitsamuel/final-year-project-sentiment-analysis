from shared.file_read_write import read_file
from shared.folders import titles_words_freq, articles_words_freq, title_monthly_frequencies, articles_monthly_frequencies, weekly_average_word_count, title_weekly_frequencies, articles_weekly_frequencies
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
import re
import json
import datetime

punctuation = r'«»‹›' + string.punctuation


def make_date_map(str_dates):
    output = {}
    for d in str_dates:
        month, year = d.split("_")
        month = int(month)
        year = int(year)
        date = datetime.datetime(year=year, month=month, day=1)
        output[d] = date
    return dict(sorted(output.items(), key=lambda item: item[1]))


def format_data(data, dates_map):
    # we got date -> all counts
    # map it to: word -> [counts...]
    output = {}
    index = 0
    for key, value in dates_map.items():
        data_at_date = data[key]
        for word, count in data_at_date.items():
            if word not in output:
                output[word] = [0 for _ in range(len(dates_map))]
            output[word][index] = count
        index += 1
    return output


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
    dates = dates_map.keys()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key, value in formatted_data.items():
        ax.plot(dates, value, label=key)
    ax.set_xlabel("Date")
    ax.set_title(
        "Most frequent word counts per month")
    ax.legend(loc='lower right')


def plot_titles_monthly():
    data = json.loads(read_file(title_monthly_frequencies))
    generate_monthly_plot(data)


def plot_articles_monthly():
    data = json.loads(read_file(articles_monthly_frequencies))
    generate_monthly_plot(data)


def plot_word_clound(file):
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


def plot_word_count_weekly():
    data = json.loads(read_file(weekly_average_word_count))
    # Sort data by week number
    data = dict(sorted(data.items(), key=lambda item: item[0]))

    # Grab x and y data
    weeks = data.keys()
    averages = []
    for key in data:
        averages.append(data[key]['average_word_count'])

    # Plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(weeks, averages)
    ax.set_xlabel("Week")
    ax.set_title(
        "Average word count per week")
    ax.legend(loc='lower right')


def plot_word_freq_weekly(file, data_source):
    data = json.loads(read_file(file))
    # Sort data by week number
    data = dict(sorted(data.items(), key=lambda item: int(item[0])))

    # Grab list of week numbers and format data in form word -> [count, count...]
    dates = data.keys()
    output_dict = format_weekly_data(data)

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key, value in output_dict.items():
        ax.plot(dates, value, label=key)
    ax.set_xlabel("Week")
    ax.set_title(
        "Most frequent word count in %s per week" % (data_source))
    ax.legend(loc='lower right')


def plot_articles_weekly():
    plot_word_freq_weekly(articles_weekly_frequencies, "article")


def plot_titles_weekly():
    plot_word_freq_weekly(title_weekly_frequencies, "title")


plot_word_count_weekly()

plot_word_clound(titles_words_freq)
plot_word_clound(articles_words_freq)

plot_articles_monthly()
plot_titles_monthly()

plot_articles_weekly()
plot_titles_weekly()
plt.show()

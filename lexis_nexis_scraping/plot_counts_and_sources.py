from shared.db_helpers import load_sources_count, load_sources, fetch_script_from_db
from shared.folders import weekly_average_word_count, monthly_average_word_count
from shared.file_read_write import read_file
from shared.dates_helper import date_from_week, date_from_month
import matplotlib.pyplot as plt
import string
import os
import json

punctuation = r'«»‹›' + string.punctuation


def plot_sources_count():
    total_sources = load_sources_count()[0][0]
    data = load_sources()

    # format our data
    sources = []
    counts = []

    for count, source in data:
        sources.append(source)
        counts.append(count)

    # Plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.barh(sources, counts, align='center', alpha=0.5)
    ax.set_xlabel("Sources")
    ax.set_ylabel("Article Count")
    ax.set_title(
        "Sources with the largest amount of articles (total %d sources)" % (total_sources))


def plot_articles_count_monthly():
    data = fetch_script_from_db("count_by_month.sql")
    formatted_data = []
    for count, month, year in data:
        formatted_data.append([date_from_month(month, year), count])

    # Sort by date
    formatted_data = sorted(formatted_data, key=lambda x: x[0])

    # format our data
    dates, counts = zip(*formatted_data)

    # Plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, counts)
    ax.set_xlabel("Date")
    ax.set_ylabel("Article Count")
    ax.set_title(
        "Number of articles published in France on COVID-19 by Month")


def plot_articles_count_weekly():
    data = fetch_script_from_db("count_by_week.sql")
    formatted_data = []
    for count, week, year in data:
        formatted_data.append([date_from_week(week, year), count])

    # Sort by date
    formatted_data = sorted(formatted_data, key=lambda x: x[0])

    # format our data
    dates, counts = zip(*formatted_data)

    # Plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, counts, label="Article Count")
    ax.set_xlabel("Date")
    ax.set_ylabel("Article Count")
    ax.set_title(
        "Number of articles published in France on COVID-19 by Week")
    ax.legend(loc='lower right')


def monthly_average_word_count_weekly(data):
    output = []
    for d in data:
        output.append([date_from_week(d['week'], d['year']),
                      d['average_word_count']])
    return sorted(output, key=lambda x: x[0])


def monthly_average_word_count_monthly(data):
    output = []
    for d in data:
        output.append([date_from_month(d['month'], d['year']),
                      d['average_word_count']])
    return sorted(output, key=lambda x: x[0])


def plot_average_word_count_monthly():
    data = json.loads(read_file(monthly_average_word_count))
    data = monthly_average_word_count_monthly(data)

    dates, counts = zip(*data)

    # Plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, counts)
    ax.set_xlabel("Date")
    ax.set_ylabel("Average word count")
    ax.set_title(
        "Average Word Count of COVID-19 French News Articles Monthly")
    ax.legend(loc='lower right')


def plot_average_word_count_weekly():
    data = json.loads(read_file(weekly_average_word_count))
    data = monthly_average_word_count_weekly(data)

    dates, counts = zip(*data)

    # Plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, counts)
    ax.set_xlabel("Date")
    ax.set_ylabel("Average word count")
    ax.set_title(
        "Average Word Count of COVID-19 French News Articles Weekly")
    ax.legend(loc='lower right')


# plot_sources_count()
# plot_articles_count_monthly()
# plot_articles_count_weekly()
plot_average_word_count_weekly()
plot_average_word_count_monthly()
plt.show()

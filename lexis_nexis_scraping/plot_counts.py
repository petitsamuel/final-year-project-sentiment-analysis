from shared.db_helpers import load_sources_count, load_sources, fetch_script_from_db
import matplotlib.pyplot as plt
import string
from datetime import datetime

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
    ax.legend(loc='lower right')

def plot_articles_count_monthly():
    data = fetch_script_from_db("count_by_month.sql")
    formatted_data = []
    for count, month, year in data:
        formatted_data.append([datetime.strptime("%d%d" % (year, month), '%Y%m'), count])

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
        "Number of articles published on COVID19 by Month")
    ax.legend(loc='lower right')

def plot_articles_count_weekly():
    data = fetch_script_from_db("count_by_week.sql")
    formatted_data = []
    for count, week, year in data:
        formatted_data.append([datetime.strptime("%d%d0" % (year, week), '%Y%W%w'), count])

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
        "Number of articles published on COVID19 by Week")
    ax.legend(loc='lower right')


# plot_sources_count()
plot_articles_count_monthly()
plot_articles_count_weekly()
plt.show()

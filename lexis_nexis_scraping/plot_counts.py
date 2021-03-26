from shared.db_helpers import load_sources_count, load_sources
import matplotlib.pyplot as plt
import string
import re
import json

punctuation = r'«»‹›' + string.punctuation


def plot_word_count_weekly():
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


plot_word_count_weekly()
plt.show()

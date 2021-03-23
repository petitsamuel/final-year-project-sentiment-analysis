from shared.variable_loader import read_file
from shared.folders import titles_words_freq, articles_words_freq, title_monthly_frequencies
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
import re
import json

punctuation = r'«»‹›' + string.punctuation


def generate_monthly_plot():
    data = json.loads(read_file(title_monthly_frequencies))
    print(data)
    # compute_title_freqs()
    # compute_articles_freqs()
    # compute_title_freqs_by_month()

    # Plot the means and variances
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.errorbar(all_folds, means, label='Mean',
    #             yerr=all_folds, uplims=True, lolims=True)
    # ax.errorbar(all_folds, variances, label='Variance',
    #             yerr=all_folds, uplims=True, lolims=True)
    # ax.set_xlabel("number of folds")
    # ax.set_title(
    #     "Variance and Mean against number of folds used. Lasso Model with C = 1")
    # ax.legend(loc='lower right')


def generate_graph(file):
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


# generate_graph(titles_words_freq)
# generate_graph(articles_words_freq)
# plt.show()
generate_monthly_plot()
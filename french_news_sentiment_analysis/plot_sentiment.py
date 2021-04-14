from shared.db_helpers import init_db, fetch_script_from_db
from shared.dates_helper import date_from_month
import matplotlib.pyplot as plt


# Plots average sentiment score for FEEL, diko and polarimots lexicons
# grouped by month.


def format_data(data):
    formatted = []
    for d in data:
        formatted.append({
            'count': d[0],
            'date': date_from_month(d[1], d[2]),
            'len': int(d[3]),
            'feel': {
                'positive_rate': float(d[4]),
                'negative_rate': float(d[5]),
                'joy': float(d[6]),
                'fear': float(d[7]),
                'sadness': float(d[8]),
                'anger': float(d[9]),
                'surprise': float(d[10]),
                'disgust': float(d[11]),
                'polarity_percent_words_used': float(d[12])
            },
            'polarimots': {
                'positive': d[13],
                'negative': d[14]
            },
            'diko': {
                'positive': d[15],
                'negative': d[16]
            }
        })
    return formatted


def get_dates(formatted_data):
    return [x['date'] for x in formatted_data]


def get_feel_data(formatted_data):
    return {
        'positive': [x['feel']['positive_rate'] for x in formatted_data],
        'negative': [x['feel']['negative_rate'] for x in formatted_data],
        'joy': [x['feel']['joy'] for x in formatted_data],
        'fear': [x['feel']['fear'] for x in formatted_data],
        'sadness': [x['feel']['sadness'] for x in formatted_data],
        'anger': [x['feel']['anger'] for x in formatted_data],
        'surprise': [x['feel']['surprise'] for x in formatted_data],
        'disgust': [x['feel']['disgust'] for x in formatted_data],
        # 'polarity_percent_words_used': [x['feel']['polarity_percent_words_used'] for x in formatted_data],
    }


def get_data_for_plot(formatted_data, source):
    return {
        'positive': [x[source]['positive'] for x in formatted_data],
        'negative': [x[source]['negative'] for x in formatted_data],
    }


def plot_feel_sentiment(feel_data, dates):
    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key, value in feel_data.items():
        ax.plot(dates, value, label=key)
    ax.set_xlabel("Date")
    ax.set_ylabel("Frequency")
    # ax.set_yscale("log")
    ax.set_title(
        "Articles Sentiment Frequencies Monthly - FEEL Lexicon")
    ax.legend(loc='lower right')


def plot_sentiment_scored(formatted_data, dates, lexicon):
    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for key, value in formatted_data.items():
        ax.plot(dates, value, label=key)
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Weighted Score")
    # ax.set_yscale("log")
    ax.set_title(
        "Articles Sentiment Frequencies Monthly - %s Lexicon" % (lexicon))
    ax.legend(loc='lower right')


def plot_all_sentiment():
    # Load data
    data = fetch_script_from_db('sentiment_rates.sql')
    formatted = format_data(data)
    del data
    # Format data
    dates = get_dates(formatted)
    feel_data = get_feel_data(formatted)
    polarimots_data = get_data_for_plot(formatted, 'polarimots')
    diko_data = get_data_for_plot(formatted, 'diko')
    # Plot data
    plot_feel_sentiment(feel_data, dates)
    plot_sentiment_scored(polarimots_data, dates, "Polarimots")
    plot_sentiment_scored(diko_data, dates, "Diko")


init_db()
plot_all_sentiment()
plt.show()

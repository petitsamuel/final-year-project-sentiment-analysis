# from shared.barthez_classifier import run_barthez_classifier
from shared.db_helpers import load_articles_feel_limited, load_articles_model_limited, init_db, update_row_sentiment_scores, commit_db_changes, has_remaining_articles_for_feel_sentiment, update_row_feel_sentiment_scores, has_remaining_articles_for_model_sentiment, update_row_barthez_sentiment_scores
from shared.lexicon_helper import load_feel_lexicon
from shared.regex_helpers import compile_regex_from_lexicon, count_intersections
from collections import Counter
from shared.text_processing import clean_text_for_analysis_lower, lemmatize_lexicon
from shared.models import FEELLexiconItem
from threading import Thread
import queue
import re


def compute_sentiment_feel(counts):
    output = FEELLexiconItem(0, 0, 0, 0, 0, 0, 0, 0, 0)
    positive_count = 0
    negative_count = 0
    for w, c in counts.items():
        try:
            feel_weights = feel_lexicon[w]
        except:
            # if word is not in lexicon - ignore it
            continue

        if feel_weights.polarity == 'positive':
            positive_count += c
        else:
            negative_count += c

        output.joy += (feel_weights.joy * c)
        output.fear += (feel_weights.fear * c)
        output.sadness += (feel_weights.sadness * c)
        output.anger += (feel_weights.anger * c)
        output.surprise += (feel_weights.surprise * c)
        output.disgust += (feel_weights.disgust * c)

    label = "positive" if positive_count > negative_count else "negative"
    print("FEEL Predicted label: %s - Score %d positive - %d negative" %
          (label, positive_count, negative_count))

    return {
        'label': label,
        'score': positive_count - negative_count,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'emotions': output
    }


def analyse_sentiment_feel(data, queue):
    output = []
    for text in data:
        cleaned_text = clean_text_for_analysis_lower(text[1])
        counts = count_intersections(re_exact_match, cleaned_text)
        output.append(compute_sentiment_feel(counts))
    queue.put(output)


# def analyse_sentiment_barthez(data, queue):
#     predictions_barthez = predict_sentiment_barthez(
#         data)
#     queue.put(predictions_barthez)


def update_db_sentiment(data, barthez, feel):
    for i in range(len(data)):
        article_id = data[i][0]
        barthez_score = 1 if barthez[i]['label'].lower() == 'positive' else 0
        feel_score = 1 if feel[i]['label'].lower() == 'positive' else 0
        update_row_sentiment_scores(article_id, barthez_score, feel_score)
    commit_db_changes()


def update_db_sentiment_feel(data, feel):
    for i in range(len(data)):
        article_id = data[i][0]
        positive_count = feel[i]['positive_count']
        negative_count = feel[i]['negative_count']
        emotions_output = feel[i]['emotions']
        update_row_feel_sentiment_scores(
            article_id, positive_count, negative_count, emotions_output)
    commit_db_changes()


def update_db_sentiment_model(data, result):
    for i in range(len(data)):
        article_id = data[i][0]
        output = 1 if result[i] == 'positive' else 0
        update_row_barthez_sentiment_scores(
            article_id, output)
    commit_db_changes()


def perform_feel_sentiment_analysis():
    data = load_articles_feel_limited(1500)  # Make batches of 1000 articles

    # use a queue to grab the return value - this makes for easy threading
    q = queue.Queue()
    analyse_sentiment_feel(data, q,)

    # Grab output
    feel_out = q.get()

    update_db_sentiment_feel(data, feel_out)
    print("Batch finished!")


def perform_model_sentiment_analysis():
    data = load_articles_model_limited(250)

    # use a queue to grab the return value - this makes for easy threading
    q = queue.Queue()
    analyse_sentiment_barthez(data, q,)

    # Grab output
    model_out = q.get()
    update_db_sentiment_model(data, model_out)
    print("Batch finished!")


def run_feel_sentiment_analysis_on_all_data():
    while has_remaining_articles_for_feel_sentiment() > 0:
        perform_feel_sentiment_analysis()
    print("Finished FEEL Sentiment Analysis")


def run_model_sentiment_analysis_on_all_data():
    while has_remaining_articles_for_model_sentiment() > 0:
        perform_model_sentiment_analysis()
    print("Finished Model Sentiment Analysis")


# Escape all strings and wrap with \b (a regex word boundary)
def text_regex_mapper(s):
    return "\\b%s\\b" % (re.escape(s))


feel_lexicon = load_feel_lexicon()
re_exact_match = compile_regex_from_lexicon(feel_lexicon)

init_db()
# run_model_sentiment_analysis_on_all_data()
run_feel_sentiment_analysis_on_all_data()

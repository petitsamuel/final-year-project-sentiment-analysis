from shared.barthez_classifier import predict_sentiment_barthez
from shared.db_helpers import load_articles_feel_limited, init_db, update_row_sentiment_scores, commit_db_changes, has_remaining_articles_for_feel_sentiment, update_row_feel_sentiment_scores
from shared.feel_lexicon_helper import load_lexicon
from collections import Counter
from shared.text_processing import clean_text_for_analysis_lower, lemmatize_lexicon
from shared.models import FEELLexiconItem
from threading import Thread
import queue
import re


def count_intersections(text, lexicon):
    output = []
    for x in lexicon:
        count = len(re.findall(r"\b" + re.escape(x) + r"\b", text))
        if count > 0:
            output.append([x, count])
    return output


def compute_sentiment_feel(counts):
    output = FEELLexiconItem(0, 0, 0, 0, 0, 0, 0, 0, 0)
    positive_count = 0
    negative_count = 0
    for w, c in counts:
        feel_weights = feel_lexicon[w]
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
        counts = count_intersections(cleaned_text, lexicon_words)
        output.append(compute_sentiment_feel(counts))
    queue.put(output)


def analyse_sentiment_barthez(data, queue):
    predictions_barthez = predict_sentiment_barthez(data)
    queue.put(predictions_barthez)


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
        positive_count = data[i]['positive_count']
        negative_count = data[i]['negative_count']
        update_row_feel_sentiment_scores(
            article_id, positive_count, negative_count)
    commit_db_changes()


def perform_sentiment_analysis():
    # use load_articles_barthez_limited for barthez analysis
    data = load_articles_feel_limited(10)  # Make batches of 100 articles

    # Pass queues as parameters to threads to grab return values
    # q = queue.Queue()
    q2 = queue.Queue()

    # thread_barthez = Thread(target=analyse_sentiment_barthez, args =(data, q,))
    thread_feel = Thread(target=analyse_sentiment_feel, args=(data, q2,))

    print("Launching threads to run analysis")
    # thread_barthez.start()
    thread_feel.start()
    # thread_barthez.join()
    thread_feel.join()
    print("All threads finished")

    # Grab outputs from threads
    # barthez_out = q.get()
    feel_out = q2.get()
    print(feel_out)
    exit() # TODO
    # update_db_sentiment(data, barthez_out, feel_out)
    update_db_sentiment_feel(data, feel_out)
    print("Done!")


def perform_feel_sentiment_analysis():
    data = load_articles_feel_limited(100)  # Make batches of 100 articles

    # use a queue to grab the return value - this makes for easy threading
    q2 = queue.Queue()
    analyse_sentiment_feel(data, q2,)

    # Grab output
    feel_out = q2.get()

    update_db_sentiment_feel(data, feel_out)
    print("Batch finished!")


def run_feel_sentiment_analysis_on_all_data():
    while has_remaining_articles_for_feel_sentiment() > 0:
        perform_sentiment_analysis()


feel_lexicon = load_lexicon()
lexicon_words = feel_lexicon.keys()

init_db()
run_feel_sentiment_analysis_on_all_data()

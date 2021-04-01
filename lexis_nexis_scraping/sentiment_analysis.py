from shared.barthez_classifier import predict_sentiment_barthez
from shared.db_helpers import load_articles_limit, init_db, update_row_sentiment_scores, commit_db_changes, has_remaining_articles_for_sentiment
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
    positive_negative_count = 0
    for w, c in counts:
        feel_weights = feel_lexicon[w]
        if feel_weights.polarity == 'positive':
            positive_negative_count = positive_negative_count + 1
        else:
            positive_negative_count = positive_negative_count - 1

        output.joy += feel_weights.joy
        output.fear += feel_weights.fear
        output.sadness += feel_weights.sadness
        output.anger += feel_weights.anger
        output.surprise += feel_weights.surprise
        output.disgust += feel_weights.disgust
    
    label = "positive" if positive_negative_count > 0 else "negative" if positive_negative_count < 0 else "neutral"
    print("FEEL Predicted label: %s - Score %d" % (label, positive_negative_count))
    
    return {
        'label': label,
        'score': positive_negative_count,
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


def perform_sentiment_analysis():
    data = load_articles_limit(100) # Make batches of 100 articles

    # Pass queues as parameters to threads to grab return values
    q = queue.Queue()
    q2 = queue.Queue()

    thread_barthez = Thread(target=analyse_sentiment_barthez, args =(data, q,))
    thread_feel = Thread(target=analyse_sentiment_feel, args = (data, q2,))

    print("Launching threads for feel and barthez sentiment analysis")
    thread_barthez.start()
    thread_feel.start()
    thread_barthez.join()
    thread_feel.join()
    print("Both threads finished")

    # Grab outputs from threads
    barthez_out = q.get()
    feel_out = q2.get()

    update_db_sentiment(data, barthez_out, feel_out)
    print("Done!")


def run_sentiment_analysis_on_all_data():
    while has_remaining_articles_for_sentiment() > 0:
        perform_sentiment_analysis()

feel_lexicon = load_lexicon()
lexicon_words = feel_lexicon.keys()

init_db()
run_sentiment_analysis_on_all_data()


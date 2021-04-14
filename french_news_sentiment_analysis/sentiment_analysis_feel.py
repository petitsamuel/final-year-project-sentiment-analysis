from shared.db_helpers import load_articles_feel_limited, init_db, update_row_sentiment_scores, commit_db_changes, has_remaining_articles_for_feel_sentiment, update_row_feel_sentiment_scores
from shared.lexicon_helper import load_feel_lexicon, compute_sentiment_feel
from shared.regex_helpers import compile_regex_from_lexicon, count_intersections
from shared.text_processing import clean_text_for_analysis_lower
from shared.models import FEELLexiconItem
from collections import Counter
from threading import Thread
import queue
import re

# This scripts performs sentiment analysis using the FEEL lexicon.
# It will fetch articles from the database which have yet to be computed
# and write the output to the database.
# It executes until there are no more articles to compute.


def analyse_sentiment_feel(data, queue):
    output = []
    for text in data:
        cleaned_text = clean_text_for_analysis_lower(text[1])
        counts = count_intersections(re_exact_match, cleaned_text)
        output.append(compute_sentiment_feel(counts, feel_lexicon))
    queue.put(output)


def update_db_sentiment_feel(data, feel):
    for i in range(len(data)):
        article_id = data[i][0]
        positive_count = feel[i]['positive_count']
        negative_count = feel[i]['negative_count']
        emotions_output = feel[i]['emotions']
        update_row_feel_sentiment_scores(
            article_id, positive_count, negative_count, emotions_output)
    commit_db_changes()


def perform_feel_sentiment_analysis():
    data = load_articles_feel_limited(2000)  # Make batches of 2000 articles

    # use a queue to grab the return value - this makes for easy threading
    # In this version of the code base - threading is not required though.
    q = queue.Queue()
    analyse_sentiment_feel(data, q,)

    # Grab output
    feel_out = q.get()

    update_db_sentiment_feel(data, feel_out)
    print("Batch finished!")


def run_feel_sentiment_analysis():
    while has_remaining_articles_for_feel_sentiment() > 0:
        perform_feel_sentiment_analysis()
    print("Finished FEEL Sentiment Analysis")


feel_lexicon = load_feel_lexicon()
re_exact_match = compile_regex_from_lexicon(feel_lexicon)

init_db()
run_feel_sentiment_analysis()

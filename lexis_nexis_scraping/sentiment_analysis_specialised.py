# from shared.barthez_classifier import run_barthez_classifier
from shared.db_helpers import load_articles_feel_limited, load_articles_model_limited, init_db, commit_db_changes, has_remaining_articles_for_feel_sentiment, update_row_feel_sentiment_specialised, add_row_counts
from shared.lexicon_helper import load_feel_lexicon, load_custom_lexicons, update_lexicon_from_specialised
from shared.regex_helpers import compile_regex_from_lexicon, count_intersections
from collections import Counter
from shared.text_processing import clean_text_for_analysis_lower
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


def analyse_sentiment(data):
    output = []
    for text in data:
        cleaned_text = clean_text_for_analysis_lower(text[1])
        # Comput matches with FEEL Lexicon
        counts_feel = count_intersections(re_exact_match, cleaned_text)
        # Compute matches with Custom Lexicons
        counts_death = count_intersections(
            specialised_lexicons.death_regexp, cleaned_text)
        counts_vaccine = count_intersections(
            specialised_lexicons.vaccine_regexp, cleaned_text)
        counts_virus = count_intersections(
            specialised_lexicons.virus_regexp, cleaned_text)

        output.append({
            'feel': compute_sentiment_feel(counts_feel),
            'death': counts_death,
            'virus': counts_virus,
            'vaccine': counts_vaccine
        })

    return output


def update_db_sentiment(data, output):
    # update articles table counts
    for i in range(len(data)):
        article_id = data[i][0]
        positive_count = output[i]['feel']['positive_count']
        negative_count = output[i]['feel']['negative_count']
        emotions_output = output[i]['feel']['emotions']
        death_count = sum(output[i]['death'].values())
        virus_count = sum(output[i]['virus'].values())
        vaccine_count = sum(output[i]['vaccine'].values())
        update_row_feel_sentiment_specialised(
            article_id, positive_count, negative_count, emotions_output, death_count, virus_count, vaccine_count)

    # Aggregate specialised word counts
    counter_death = Counter()
    counter_virus = Counter()
    counter_vaccine = Counter()
    for d in output:
        counter_death += d['death']
        counter_virus += d['virus']
        counter_vaccine += d['vaccine']

    # Insert row and commit changes
    add_row_counts(counter_death, counter_vaccine, counter_virus)
    commit_db_changes()


def perform_sentiment_analysis():
    data = load_articles_feel_limited(100)
    output = analyse_sentiment(data)

    update_db_sentiment(data, output)
    print("Batch finished!")


def run_feel_sentiment_analysis_on_all_data():
    while has_remaining_articles_for_feel_sentiment() > 0:
        perform_sentiment_analysis()
        exit()
    print("Finished FEEL Sentiment Analysis")


# Load FEEL and specialised lexicons
specialised_lexicons = load_custom_lexicons()
feel_lexicon = load_feel_lexicon()

# Update FEEL lexicon (remove terms from specialised lexicons)
feel_lexicon = update_lexicon_from_specialised(
    feel_lexicon, specialised_lexicons)

re_exact_match = compile_regex_from_lexicon(feel_lexicon)

init_db()
run_feel_sentiment_analysis_on_all_data()

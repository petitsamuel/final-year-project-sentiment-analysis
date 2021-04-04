from shared.lexicon_helper import load_polarimots_lexicon, compute_sentiment
from shared.db_helpers import commit_db_changes, load_articles_barthez_limited, has_remaining_articles_polarimots, update_row_polarimots_sentiment_scores
from shared.regex_helpers import compile_regex_from_lexicon


def process_counts_polimots(counts):
    negative_count = 0
    positive_count = 0
    for word, count in counts.items():
        try:
            lexicon_word = lexicon[word]
        except:
            # if word is not in lexicon - ignore it
            continue

        score = lexicon_word.polarity * lexicon_word.reliability * count
        if lexicon_word.polarity == 1:
            positive_count += score
        elif lexicon_word.polarity == -1:
            negative_count += score
    score = negative_count + positive_count
    label = "positive" if score > 0 else "negative"
    print("Polarimots Predicted label: %s --- %.2f Total Score - %.2f positive - %.2f negative" %
          (label, score, positive_count, negative_count))

    return {
        'label': label,
        'score': score,
        'positive_count': positive_count,
        'negative_count': negative_count,
    }


def update_db_sentiment_polarimots(data, output):
    for i in range(len(data)):
        article_id = data[i][0]
        update_row_polarimots_sentiment_scores(
            article_id, output[i]['positive_count'], output[i]['negative_count'])
    commit_db_changes()


def run_polarimots_sentiment_analysis():
    while has_remaining_articles_polarimots() > 0:
        data = load_articles_barthez_limited(2000)
        out = compute_sentiment(data, re_exact_match, process_counts_polimots)
        update_db_sentiment_polarimots(data, out)
        print("Batch finished!")


# Load lexicon and regex pattern matcher
lexicon = load_polarimots_lexicon()
re_exact_match = compile_regex_from_lexicon(lexicon)

run_polarimots_sentiment_analysis()

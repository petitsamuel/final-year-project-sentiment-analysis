from shared.lexicon_helper import load_polarimots_lexicon
from shared.db_helpers import load_articles_barthez_limited
from shared.regex_helpers import compile_regex_from_lexicon, count_intersections
from shared.text_processing import clean_text_for_analysis_lower


def compute_sentiment(data):
    output = []
    for text in data:
        cleaned_text = clean_text_for_analysis_lower(text[1])
        counts = count_intersections(re_exact_match, cleaned_text)
        print(counts)
        exit()
        # output.append(compute_sentiment_feel(counts))
    queue.put(output)


def run_polarimots_sentiment_analysis():
    data = load_articles_barthez_limited(1)

    out = compute_sentiment(data)
    print(out)
    # update_db_sentiment_feel(data, feel_out)
    print("Batch finished!")


# Load lexicon and regex pattern matcher
lexicon = load_polarimots_lexicon()
re_exact_match = compile_regex_from_lexicon(lexicon)

run_polarimots_sentiment_analysis()

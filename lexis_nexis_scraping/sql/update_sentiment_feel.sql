UPDATE articles
SET feel_sentiment_positive = %s,
    feel_sentiment_negative = %s
WHERE id = %s;
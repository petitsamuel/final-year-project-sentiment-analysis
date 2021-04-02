SELECT count(*)
FROM articles
WHERE feel_sentiment_positive IS NULL
    AND feel_sentiment_negative IS NULL;
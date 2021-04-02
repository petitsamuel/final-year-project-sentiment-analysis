SELECT count(*)
FROM articles
WHERE feel_sentiment_positive IS NOT NULL
    AND feel_sentiment_negative;
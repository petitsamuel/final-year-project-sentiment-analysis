SELECT id,
    body
FROM articles
WHERE feel_sentiment_positive IS NULL
    OR feel_sentiment_negative IS NULL
    OR barthez_sentiment IS NULL
LIMIT %s;
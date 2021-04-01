SELECT id,
    body
FROM articles
WHERE feel_sentiment IS NULL
    OR barthez_sentiment IS NULL
LIMIT %s;
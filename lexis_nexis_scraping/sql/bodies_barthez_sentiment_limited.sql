SELECT id,
    body
FROM articles
WHERE barthez_sentiment IS NULL
LIMIT %s;
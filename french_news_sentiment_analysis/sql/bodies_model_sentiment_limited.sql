SELECT id,
    body
FROM articles
WHERE barthez_sentiment IS NULL
ORDER BY RAND()
LIMIT %s;
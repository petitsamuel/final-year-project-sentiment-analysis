UPDATE articles
SET feel_sentiment = %s,
    barthez_sentiment = %s
WHERE id = %s;
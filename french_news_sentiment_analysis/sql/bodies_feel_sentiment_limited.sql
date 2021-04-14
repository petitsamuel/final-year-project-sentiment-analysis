SELECT id,
    body
FROM articles
WHERE feel_sentiment_positive IS NULL
    OR feel_sentiment_negative IS NULL
    OR feel_anger IS NULL
    OR feel_disgust IS NULL
    OR feel_fear IS NULL
    OR feel_joy IS NULL
    OR feel_sadness IS NULL
    OR feel_surprise IS NULL
-- ORDER BY RAND()
LIMIT %s;
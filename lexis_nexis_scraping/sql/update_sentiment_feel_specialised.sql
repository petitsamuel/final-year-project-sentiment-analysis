UPDATE articles
SET feel_sentiment_positive = %s,
    feel_sentiment_negative = %s,
    feel_joy = %s,
    feel_fear = %s,
    feel_sadness = %s,
    feel_anger = %s,
    feel_surprise = %s,
    feel_disgust = %s,
    death_sentiment = %s,
    virus_sentiment = %s,
    vaccine_sentiment = %s
WHERE id = %s;
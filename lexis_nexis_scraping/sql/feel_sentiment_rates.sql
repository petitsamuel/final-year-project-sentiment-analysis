SELECT COUNT(*),
    MONTH(date),
    YEAR(date),
    SUM(length) AS TOTAL_LENGTH,
    SUM(feel_sentiment_positive) / SUM(length) AS POSITIVE_RATE,
    SUM(feel_sentiment_negative) / SUM(length) AS NEGATIVE_RATE,
    SUM(feel_joy) / SUM(length) AS JOY,
    SUM(feel_fear) / SUM(length) AS FEAR,
    SUM(feel_sadness) / SUM(length) AS SADNESS,
    SUM(feel_anger) / SUM(length) AS ANGER,
    SUM(feel_surprise) / SUM(length) AS SURPRISE,
    SUM(feel_disgust) / SUM(length) AS DISGUST,
    (
        SUM(feel_sentiment_negative) + SUM(feel_sentiment_positive)
    ) * 100 / SUM(length) AS PERCENT_WORDS_USED_POLARITY
FROM articles
WHERE feel_joy IS NOT NULL
    AND feel_sentiment_positive IS NOT NULL
    AND feel_sentiment_negative IS NOT NULL
    AND feel_fear IS NOT NULL
    AND feel_sadness IS NOT NULL
    AND feel_anger IS NOT NULL
    AND feel_surprise IS NOT NULL
    AND feel_disgust IS NOT NULL
GROUP BY MONTH(date),
    YEAR(date)
ORDER BY YEAR(date),
    MONTH(date);
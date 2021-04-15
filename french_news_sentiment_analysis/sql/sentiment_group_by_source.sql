SELECT COUNT(*),
    source,
    SUM(length) AS TOTAL_LENGTH,
    SUM(feel_sentiment_positive) / SUM(length) AS POSITIVE_RATE,
    SUM(feel_sentiment_negative) / SUM(length) AS NEGATIVE_RATE,
    SUM(feel_joy) / SUM(length) AS JOY,
    SUM(feel_fear) / SUM(length) AS FEAR,
    SUM(feel_sadness) / SUM(length) AS SADNESS,
    SUM(feel_anger) / SUM(length) AS ANGER,
    SUM(feel_surprise) / SUM(length) AS SURPRISE,
    SUM(feel_disgust) / SUM(length) AS DISGUST -- SUM(polarimots_positive) / SUM(length) as POLARIMOTS_POSITIVE,
    -- SUM(ABS(polarimots_negative)) / SUM(length) as POLARIMOTS_NEGATIVE,
    -- SUM(diko_positive) / SUM(length) as DIKO_POS,
    -- SUM(ABS(diko_negative)) / SUM(length) as DIKO_NEGATIVE
FROM articles
WHERE feel_joy IS NOT NULL
    AND feel_sentiment_positive IS NOT NULL
    AND feel_sentiment_negative IS NOT NULL
    AND feel_fear IS NOT NULL
    AND feel_sadness IS NOT NULL
    AND feel_anger IS NOT NULL
    AND feel_surprise IS NOT NULL
    AND feel_disgust IS NOT NULL
    AND diko_positive IS NOT NULL
    AND diko_negative IS NOT NULL
GROUP BY source
ORDER BY count(*) ASC;
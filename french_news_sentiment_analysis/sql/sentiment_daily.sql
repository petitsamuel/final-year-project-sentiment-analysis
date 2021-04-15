SELECT DAY(date),
    MONTH(date),
    YEAR(date),
    SUM(length) AS TOTAL_LENGTH,
    SUM(feel_sentiment_positive) AS POSITIVE_SUM,
    SUM(feel_sentiment_negative) AS NEGATIVE_SUM,
    SUM(feel_joy) AS JOY,
    SUM(feel_fear) AS FEAR,
    SUM(feel_sadness) AS SADNESS,
    SUM(feel_anger) AS ANGER,
    SUM(feel_surprise) AS SURPRISE,
    SUM(feel_disgust) AS DISGUST -- , SUM(polarimots_positive) / SUM(length) as POLARIMOTS_POSITIVE,
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
GROUP BY DAY(date),
    MONTH(date),
    YEAR(date)
ORDER BY YEAR(date),
    MONTH(date),
    DAY(date),
    YEAR(date);
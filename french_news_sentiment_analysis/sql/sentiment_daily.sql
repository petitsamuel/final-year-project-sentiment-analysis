SELECT DAY(date),
    MONTH(date),
    YEAR(date),
    SUM(length) AS TOTAL_LENGTH,
    SUM(CAST(feel_sentiment_positive AS DECIMAL(10, 8))) / SUM(length) AS POSITIVE,
    SUM(CAST(feel_sentiment_negative AS DECIMAL(10, 8))) / SUM(length) AS NEGATIVE,
    SUM(CAST(feel_joy AS DECIMAL(10, 8))) / SUM(length) AS JOY,
    SUM(CAST(feel_fear AS DECIMAL(10, 8))) / SUM(length) AS FEAR,
    SUM(CAST(feel_sadness AS DECIMAL(10, 8))) / SUM(length) AS SADNESS,
    SUM(CAST(feel_anger AS DECIMAL(10, 8))) / SUM(length) AS ANGER,
    SUM(CAST(feel_surprise AS DECIMAL(10, 8))) / SUM(length) AS SURPRISE,
    SUM(CAST(feel_disgust AS DECIMAL(10, 8))) / SUM(length) AS DISGUST -- , SUM(polarimots_positive) / SUM(length) as POLARIMOTS_POSITIVE,
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
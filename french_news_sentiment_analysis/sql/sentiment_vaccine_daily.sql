SELECT COUNT(*),
    SUM(vaccine_sentiment),
    SUM(vaccine_sentiment) / COUNT(*) AS AVG_VACCINE_SENTIMENT,
    SUM(vaccine_sentiment) / SUM(length) AS AVG_VACCINE_WORD,
    DAY(date),
    MONTH(date),
    YEAR(date)
FROM articles
GROUP BY DAY(date),
    MONTH(date),
    YEAR(date)
ORDER BY YEAR(date),
    MONTH(date),
    DAY(date),
    YEAR(date);
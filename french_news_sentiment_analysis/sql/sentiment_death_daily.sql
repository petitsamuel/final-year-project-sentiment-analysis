SELECT COUNT(*),
    SUM(death_sentiment),
    SUM(death_sentiment) / COUNT(*) AS AVG_DEATH_SENTIMENT,
    SUM(death_sentiment) / SUM(length) AS AVG_DEATH_FREQ,
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
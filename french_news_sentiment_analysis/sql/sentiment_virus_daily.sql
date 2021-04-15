SELECT COUNT(*),
    SUM(virus_sentiment),
    SUM(virus_sentiment) / COUNT(*) AS AVG_VIRUS_SENTIMENT,
    SUM(virus_sentiment) / SUM(length) AS AVG_VIRUS_WORD,
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
SELECT SUM(vaccine_sentiment) / SUM(length),
    SUM(virus_sentiment) / SUM(length),
    SUM(death_sentiment) / SUM(length),
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
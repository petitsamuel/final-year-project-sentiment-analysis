SELECT SUM(vaccine_sentiment),
    SUM(virus_sentiment),
    SUM(death_sentiment),
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
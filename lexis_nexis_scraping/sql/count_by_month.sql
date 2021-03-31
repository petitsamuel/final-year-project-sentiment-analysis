SELECT COUNT(id),
    MONTH(date),
    YEAR(date)
FROM articles
GROUP BY MONTH(date),
    YEAR(date);

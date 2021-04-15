SELECT COUNT(id),
    WEEK(date),
    YEAR(date)
FROM articles
GROUP BY WEEK(date),
    YEAR(date);
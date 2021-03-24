SELECT count(id),
    SUM(length),
    WEEK(date)
FROM articles
WHERE YEAR(date) = 2021
GROUP BY WEEK(date);

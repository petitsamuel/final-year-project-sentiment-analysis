SELECT title,
    MONTH(date),
    YEAR(date)
FROM articles
WHERE YEAR(date) = 2021;

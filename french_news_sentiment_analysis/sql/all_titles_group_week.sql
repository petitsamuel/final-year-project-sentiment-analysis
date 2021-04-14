SELECT title,
    WEEK(date)
FROM articles
WHERE YEAR(date) = 2021;
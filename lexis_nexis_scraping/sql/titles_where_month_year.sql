SELECT title
FROM articles
WHERE MONTH(date) = %s
    AND YEAR(date) = %s
ORDER BY RAND()
LIMIT %s;
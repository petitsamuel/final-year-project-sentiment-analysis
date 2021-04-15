SELECT a.id as id_1,
    a.title
FROM articles a
    INNER JOIN (
        SELECT title
        FROM articles
        GROUP BY title
        HAVING COUNT(title) > 1
    ) dup ON a.title = dup.title;
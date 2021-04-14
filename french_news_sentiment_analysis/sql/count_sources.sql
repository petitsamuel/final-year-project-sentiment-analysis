SELECT COUNT(*)
FROM (
        SELECT DISTINCT source
        FROM articles
    ) AS sources
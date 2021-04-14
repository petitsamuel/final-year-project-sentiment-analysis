SELECT id,
    body
FROM articles
WHERE diko_positive IS NULL
    OR diko_negative IS NULL
ORDER BY RAND()
LIMIT %s;
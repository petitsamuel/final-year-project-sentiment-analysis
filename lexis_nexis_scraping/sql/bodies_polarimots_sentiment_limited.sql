SELECT id,
    body
FROM articles
WHERE polarimots_positive IS NULL
    OR polarimots_negative IS NULL
LIMIT %s;
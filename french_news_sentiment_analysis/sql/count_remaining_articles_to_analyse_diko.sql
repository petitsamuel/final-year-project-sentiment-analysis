SELECT count(*)
FROM articles
WHERE diko_positive IS NULL
    OR diko_negative IS NULL;
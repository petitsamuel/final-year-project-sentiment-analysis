UPDATE articles
SET diko_positive = %s,
    diko_negative = %s
WHERE id = %s;
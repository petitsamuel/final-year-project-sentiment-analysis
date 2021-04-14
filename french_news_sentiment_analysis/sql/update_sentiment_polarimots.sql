UPDATE articles
SET polarimots_positive = %s,
    polarimots_negative = %s
WHERE id = %s;
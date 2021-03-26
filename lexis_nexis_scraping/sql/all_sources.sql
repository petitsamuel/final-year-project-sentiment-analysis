SELECT COUNT(*),
    source
FROM articles
GROUP BY source
ORDER BY count(id) DESC
LIMIT 30;
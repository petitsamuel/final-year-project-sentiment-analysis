SELECT COUNT(*),
    source,
    SUM(length) AS TOTAL_LENGTH,
    SUM(length) / COUNT(*) AS AVERAGE_WORD_COUNT
FROM articles
GROUP BY source
ORDER BY count(*) ASC;
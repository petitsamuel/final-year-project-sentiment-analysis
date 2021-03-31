SELECT SUM(length) AS word_sum,
    COUNT(id) AS article_count,
    ROUND(sum(length) / count(id)) AS average_words,
    MONTH(date),
    YEAR(date)
FROM articles
GROUP BY YEAR(date),
    MONTH(date);
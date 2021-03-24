SELECT SUM(length) AS word_sum,
    COUNT(id) AS article_count,
    round(sum(length) / count(id)) AS average_words,
    WEEK(date)
FROM articles
WHERE YEAR(date) = 2021
GROUP BY WEEK(date);

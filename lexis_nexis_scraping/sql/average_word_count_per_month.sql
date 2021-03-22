SELECT SUM(length) AS word_sum,
    COUNT(id) AS article_count,
    round(sum(length) / count(id)) AS average_words,
    MONTH(date),
    YEAR(date)
from articles
GROUP BY MONTH(date),
    YEAR(date);

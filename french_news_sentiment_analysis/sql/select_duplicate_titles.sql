SELECT a.id as id_1,
    a.title
FROM articles a
    INNER JOIN (
        SELECT title
        FROM articles
        GROUP BY title
        HAVING COUNT(title) > 1
    ) dup ON a.title = dup.title;
-- SELECT 
--     articles.id, articles.title, articles.source
-- FROM 
--     articles
-- INNER JOIN 
--     articles from_source ON (from_source.title = articles.title)
-- WHERE 
--     from_source.source = articles.source;
-- select length,
--     feel_sentiment_positive,
--     feel_sentiment_negative,
--     polarimots_positive,
--     polarimots_negative,
--     diko_positive,
--     diko_negative
-- from articles INTO OUTFILE '/var/lib/mysql-files/monthlysentiment.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
-- select month(date),
--     year(date),
--     sum(length),
--     avg(feel_sentiment_positive / length),
--     stddev(feel_sentiment_positive / length),
--     avg(feel_sentiment_negative / length),
--     stddev(feel_sentiment_negative / length),
--     avg(feel_joy / length),
--     stddev(feel_joy / length),
--     avg(feel_fear / length),
--     stddev(feel_fear / length),
--     avg(feel_sadness / length),
--     stddev(feel_sadness / length),
--     avg(feel_anger / length),
--     stddev(feel_anger / length),
--     avg(feel_surprise / length),
--     stddev(feel_surprise / length),
--     avg(feel_disgust / length),
--     stddev(feel_disgust / length),
--     avg(death_sentiment / length),
--     stddev(death_sentiment / length),
--     avg(virus_sentiment / length),
--     stddev(virus_sentiment / length),
--     avg(vaccine_sentiment / length),
--     stddev(vaccine_sentiment / length)
-- from articles
-- group by month(date),
--     year(date)
-- order by year(date),
--     month(date) INTO OUTFILE '/var/lib/mysql-files/monthlysentiment.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
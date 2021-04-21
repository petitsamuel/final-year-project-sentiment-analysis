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
-- select 
--     length,
--     feel_sentiment_positive,
--     feel_sentiment_negative,
--     feel_joy,
--     feel_fear,
--     feel_sadness,
--     feel_anger,
--     feel_surprise,
--     feel_disgust
-- from articles INTO OUTFILE '/var/lib/mysql-files/feel_stat_overview.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
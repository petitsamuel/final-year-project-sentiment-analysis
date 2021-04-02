ALTER TABLE articles
ADD COLUMN feel_sentiment_positive INT DEFAULT NULL,
    ADD COLUMN feel_sentiment_negative INT DEFAULT NULL,
    ADD COLUMN barthez_sentiment TINYINT(1) DEFAULT NULL;
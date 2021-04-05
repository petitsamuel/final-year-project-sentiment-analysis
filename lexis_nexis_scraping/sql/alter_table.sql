ALTER TABLE articles
ADD COLUMN feel_sentiment_positive INT DEFAULT NULL,
    ADD COLUMN feel_sentiment_negative INT DEFAULT NULL,
    ADD COLUMN polarimots_positive FLOAT DEFAULT NULL,
    ADD COLUMN polarimots_negative FLOAT DEFAULT NULL,
    ADD COLUMN feel_joy INT DEFAULT NULL,
    ADD COLUMN feel_fear INT DEFAULT NULL,
    ADD COLUMN feel_sadness INT DEFAULT NULL,
    ADD COLUMN feel_anger INT DEFAULT NULL,
    ADD COLUMN feel_surprise INT DEFAULT NULL,
    ADD COLUMN feel_disgust INT DEFAULT NULL,
    ADD COLUMN barthez_sentiment TINYINT(1) DEFAULT NULL,
    ADD COLUMN diko_positive FLOAT DEFAULT NULL,
    ADD COLUMN diko_negative FLOAT DEFAULT NULL;
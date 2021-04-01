from shared.barthez_classifier import predict_sentiment_barthez
from shared.db_helpers import load_articles_limit, init_db

def predict_articles_sentiments():
    init_db()
    data = load_articles_limit()
    predictions_barthez = predict_sentiment_barthez(data)
    print(predictions_barthez)


predict_articles_sentiments()
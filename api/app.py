import tweepy
from textblob import TextBlob
import re
from flask import Flask
from flask_restful import Resource, Api
import os
from dotenv import load_dotenv
from util.TweetProcessing import (
    get_tweets,
    get_tweet_sentiment,
    count_frequency_tweet_sentiments,
)
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={r"/predict/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


class tweet_process_and_compute_result(Resource):
    @cross_origin()
    def get(self, username):
        # to check for 404 error
        try:
            tweets_to_check_for = get_tweets(username)
        except:
            return {"error": "Username does not exist. Check again for possible typo."}

        sentiments_collections = []
        result = []

        for tweet in tweets_to_check_for:
            sentiments_collections.append(get_tweet_sentiment(tweet))

        sentiments_result = count_frequency_tweet_sentiments(sentiments_collections)

        positive_sentiment = 0
        negative_sentiment = 0

        for key, value in sentiments_result.items():
            if key == "positive":
                positive_sentiment = value
            elif key == "negative":
                negative_sentiment = value

        statement = "final remark on username"

        if negative_sentiment / positive_sentiment > 1:
            neg_value_in_percentage = round(
                (negative_sentiment / positive_sentiment) * 100
            )
            statement = (
                username + " has negative tweets with " + neg_value_in_percentage + "%"
            )
        else:
            statement = username + " is safe to interact with"

        sentiments_result["remark"] = statement
        result.append(sentiments_result)
        return result


api.add_resource(tweet_process_and_compute_result, "/predict/<username>")


# Driver function
if __name__ == "__main__":
    app.run(debug=True)

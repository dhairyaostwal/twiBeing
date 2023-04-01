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

# Driver function
if __name__ == "__main__":

    # checking tweets for particular username
    username = "jordanbpeterson"
    
    tweets_to_check_for = get_tweets(username)

    sentiments_collections = []

    for tweet in tweets_to_check_for:
        sentiments_collections.append(get_tweet_sentiment(tweet))

    result = count_frequency_tweet_sentiments(sentiments_collections)
    print(result)

    positive_sentiment = 0
    negative_sentiment = 0

    for key, value in result.items():
        if key == "positive":
            positive_sentiment = value
        elif key == "negative":
            negative_sentiment = value

    if negative_sentiment / positive_sentiment > 1:
        neg_value_in_percentage = round((negative_sentiment / positive_sentiment) * 100)
        print("ALERT!\nNegativity of Tweets =", neg_value_in_percentage, "%")

    print("CONCLUSION:\nAccount Username -", username, "is safe to interact with")

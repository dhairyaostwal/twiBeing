import tweepy
from textblob import TextBlob
import re

consumer_key = "add yours"
consumer_secret = "add yours"
access_key = "add yours"
access_secret = "add yours"

# Function to extract tweets
def get_tweets(username):

    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets = 200
    # tweets = api.user_timeline(screen_name=username)
    # for i in range(number_of_tweets):
    #     tweets = api.user_timeline(screen_name=username, page = i)
    tweets = api.user_timeline(screen_name=username, count=number_of_tweets)

    # Empty Array
    tmp = []
    for t in tweets:
        tmp.append(t.text)

    return tmp


def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    """
    return " ".join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()
    )


def get_tweet_sentiment(tweet):
    """
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def count_frequency_tweet_sentiments(my_list):
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1

    return freq

# Driver function
if __name__ == "__main__":

    # checking tweets for particular username
    username = "jordanbpeterson"
    # username = "narendramodi"
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

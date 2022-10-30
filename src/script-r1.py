from distutils.command.clean import clean
import tweepy
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
    number_of_tweets = 100
    # tweets = api.user_timeline(screen_name=username)
    # for i in range(number_of_tweets):
    #     tweets = api.user_timeline(screen_name=username, page = i)
    no_of_pages = 10
    for i in range(no_of_pages):
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


# def remove_empty_tweets(tweet):
#     if len(tweet)==0:


# Driver code
if __name__ == "__main__":

    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    tweet_collection = get_tweets("narendramodi")
    print(tweet_collection)
    n = len(tweet_collection)

    print("-" * 50)

    result_post_cleaning = []
    for tweet in tweet_collection:
        result_post_cleaning.append(clean_tweet(tweet))

    print(result_post_cleaning)

    print("Number of tweets", n)

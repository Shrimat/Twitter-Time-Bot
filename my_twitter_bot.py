import tweepy
import time
from datetime import datetime

FILE_NAME = "last_seen_id.txt"
DEFAULT_MESSAGE = "Hey, I see you want the time? The time of this reply is: "
HASH_TAG = "#timeplease"
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_last_tweet_id():
    f = open(FILE_NAME, "r")
    last_id = f.read()
    f.close()
    return last_id


# Last ID for testing: 1311627360924565505
def update_last_tweet_id(new_id):
    f = open(FILE_NAME, "w")
    f.write(str(new_id))
    f.close()


def check_asked_time():
    my_tweets = api.mentions_timeline(get_last_tweet_id())
    if my_tweets:
        update_last_tweet_id(my_tweets[-1].id)
    for tweet in reversed(my_tweets):
        if HASH_TAG in tweet.text.lower():
            print("Found a request, answering...")
            print(tweet.created_at)
            current_time = datetime.now().strftime("%H:%M")
            api.update_status(status=DEFAULT_MESSAGE + current_time,
                              in_reply_to_status_id=tweet.id,
                              auto_populate_reply_metadata=True)


while True:
    check_asked_time()
    time.sleep(30)

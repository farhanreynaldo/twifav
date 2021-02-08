from datetime import date
import json
from pathlib import Path

import tweepy
from tweepy.api import API

from tweet import parse_tweet
from utils import dump_jsonl, get_last_tweet_id, update_last_tweet_id

PROJECT_ROOT = Path.cwd()
REMOTE_PATH = "/home/runner/secrets/secrets.json"
RECENT_TWEET_ID_PATH = PROJECT_ROOT / "last_tweet_id.json"


def authenticate_with_secrets(local=False) -> API:
    secret_filepath = PROJECT_ROOT / "secrets.json" if local else REMOTE_PATH
    secret_file = open(secret_filepath)
    secret_data = json.load(secret_file)
    CONSUMER_KEY = secret_data["API_KEY"]
    CONSUMER_SECRET = secret_data["API_SECRET"]
    ACCESS_TOKEN = secret_data["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = secret_data["ACCESS_SECRET"]
    secret_file.close()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api


def main():
    OUTPUT_PATH = PROJECT_ROOT / "data" / f"{date.today().isoformat()}.jl"
    api = authenticate_with_secrets()

    last_tweet_id = get_last_tweet_id(RECENT_TWEET_ID_PATH)
    faves = api.favorites(count=50, tweet_mode="extended", since_id=last_tweet_id)

    if faves:
        tweets = [parse_tweet(tweet) for tweet in faves]
        dump_jsonl(tweets, OUTPUT_PATH, append=True)
        update_last_tweet_id(faves[0].id, RECENT_TWEET_ID_PATH)


if __name__ == "__main__":
    main()

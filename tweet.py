from typing import Dict, Any, List
from tweepy.models import Status
from datetime import datetime

JSON = Dict[str, Any]
DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"


def parse_tweet(tweet_raw: Status) -> JSON:
    tweet = tweet_raw._json
    return {
        "created_at": tweet["created_at"],
        "timestamp": datetime.strptime(tweet["created_at"], DATE_FORMAT).isoformat(),
        "id": tweet["id"],
        "id_str": tweet["id_str"],
        "full_text": tweet["full_text"],
        "urls": parse_urls(tweet),
        "images": parse_images(tweet),
        "user_id": tweet["user"]["id"],
        "username": tweet["user"]["screen_name"],
        "link": f"https://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}",
    }


def parse_urls(tweet: JSON) -> List[str]:
    try:
        return [url["expanded_url"] for url in tweet["entities"]["urls"]]
    except KeyError:
        return []


def parse_images(tweet: JSON) -> List[str]:
    try:
        return [
            img["media_url_https"]
            for img in tweet["entities"]["media"]
            if img["type"] == "photo" and img["expanded_url"].find("/photo/") != -1
        ]
    except KeyError:
        return []

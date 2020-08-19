import tweepy
import json
import pandas as pd 

twitter_credential_path = 'creds.json'
with open(twitter_credential_path, "r") as json_file:
    twitter_creds = json.load(json_file)

# Daten aus der JSON Datei
CONSUMER_KEY = twitter_creds["consumer_key"]
CONSUMER_SECRET = twitter_creds["consumer_secret"]
ACCESS_KEY = twitter_creds["access_key"]
ACCESS_SECRET = twitter_creds["access_secret"]

# Authentifizierung
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(
    auth, 
    wait_on_rate_limit=True, 
    wait_on_rate_limit_notify=True
    )
#api.update_status("Kleiner API Test")

def get_followers():
    screen_name = "kulturdata"
    followers = tweepy.Cursor(api.followers, screen_name) 
    _dict = {}
    for follower in followers.items(10): 
        _dict[follower.screen_name] = int(follower.followers_count)
    return _dict

def save_as_csv():
    db = pd.read_csv("db.csv").to_dict()
    db.update(_dict)


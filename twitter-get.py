import tweepy
import json
import pandas as pd 
import datetime

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
    date_list = []
    user_list = []
    follower_list = []

    for follower in followers.items(2): 
        print(follower)
        date_list.append(datetime.datetime.today().strftime("%Y-%m-%d"))
        user_list.append(follower.screen_name)
        follower_list.append(int(follower.followers_count))
        

    _dict['date'] = date_list
    _dict['user'] = user_list
    _dict['follower'] = follower_list

    # Dict --> DataFrame
    data = pd.DataFrame.from_dict(_dict)

    # DataFrame --> CSV File
    data.to_csv('db.csv', mode='a', header=False)




if __name__ == "__main__":
    get_followers()

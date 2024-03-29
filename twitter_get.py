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

def get_followers():
    screen_name = "kulturdata"
    followers = tweepy.Cursor(api.followers, screen_name) 

    _dict = {}
    date_list = []
    user_list = []
    follower_list = []

    for follower in followers.items(): 
        date_list.append(datetime.datetime.today().strftime("%Y-%m-%d"))
        user_list.append(follower.screen_name)
        follower_list.append(int(follower.followers_count))
        
    _dict['date'] = date_list
    _dict['user'] = user_list
    _dict['follower'] = follower_list

    # Dict --> DataFrame
    data = pd.DataFrame.from_dict(_dict)

    # DataFrame --> CSV File
    data.to_csv('db.csv', mode='a', header=False, index=False)

def get_2_most_recent_data():
    data = pd.read_csv('db.csv')
    data['date'] = pd.to_datetime(data['date']) #dtype manipulation to datetime
    data['follower'] = pd.to_numeric(data['follower']) #dtype manipulation to integer
    
    date_group_by = data.groupby(data['date']).sum()

    recent_date = data['date'].max()
    recent_followers = data.loc[data['date'] == recent_date ] # newest rows
    recent_followers.reset_index(drop=True, inplace=True)
    
    second_date = data['date'].drop_duplicates().nlargest(2).iloc[-1]
    second_recent_followers = data.loc[data['date'] == second_date ] # second newest row
    second_recent_followers.reset_index(drop=True, inplace=True)
    return recent_followers, second_recent_followers

def calculate_growth():
    recent_followers, second_recent_followers = get_2_most_recent_data()

    new_dict = {}
    for user in recent_followers['user']:
        try:
            follower_count = recent_followers.loc[recent_followers['user'] == user].iloc[0]['follower']
            follower_count_2 = second_recent_followers.loc[second_recent_followers['user'] == user].iloc[0]['follower']
            diff = follower_count - follower_count_2

            if diff > 0 and follower_count > 0: # make sure there is no division / 0  and no negative numbers
                new_dict[user] = round((diff/follower_count) * 100, 2) # absolute values always prefer th big accounts
        except:
            pass
    return new_dict

def tweet():
    new_dict = calculate_growth()
    ordered_dict = {k: v for k, v in sorted(new_dict.items(), key=lambda item: item[1], reverse=True)} #not mine but works fine
    top_user = list(ordered_dict.keys())
    top_growth = list(ordered_dict.values()) 
    text = f'''
    Top3 meiner Follower mit größtem Wachstum 🚀 (7 Tage):
    Platz 1: @{top_user[0]} + {top_growth[0]}% 
    Platz 2: @{top_user[1]} + {top_growth[1]}%
    Platz 3: @{top_user[2]} + {top_growth[2]}%
    Gratulation! 🎊
    '''
    print (text, "\nZeichenanzahl:", len(text), flush=True)
    api.update_status(text)

if __name__ == "__main__":
    # get_followers()
    calculate_growth()
    tweet()

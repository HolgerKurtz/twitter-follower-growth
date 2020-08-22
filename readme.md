# Congratulate your Top3 Followers on Twitter

This twitter bot scans your followers every 7 days, calculates their growth and congratulates them on twitter.

## Requirements
```bash
virtualenv env
source env/bin/activate
pip3 install tweepy pandas
```

## Customization
- Get yourself some credits to use a twitter bot from developer.twitter.com
- Create a file creds.json and input your credentials like this:
```json
{"consumer_key": "KEY",
    "consumer_secret": "KEY", 
    "access_key": "KEY", 
    "access_secret": "KEY"
}
```
- Input your twitter handle:
```python
screen_name = "YOUR USER NAME WITHOUT @" 
```
- Create a file called db.csv and input the headers: date,user,follower


## How to use
```bash
pip3 twitter-get.py
```
- Create a cron job to run this script once every 7 days
- I host everything on pythonanywhere.com (it's free!)


## First Time
When running the script for the first time, it's recommended to comment out this line to prevent a useless tweet:
```python 
#api.update_status(text) 
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
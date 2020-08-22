import datetime
import sys
today = datetime.date.today()
weekday = today.weekday()

print ("Weekday:", weekday, flush=True)

if weekday == 1: # if sunday
    import twitter_get

    twitter_get.get_followers()
    twitter_get.calculate_growth()
    twitter_get.tweet()
else:
    print (f'Nothing to do at: {today}')
    sys.exit()
    

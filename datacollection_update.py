# Collecting tweets from an account and compare with the previously collected
# tweets and update the file with only new tweets.

from twython import Twython
import sys
import time
import json
import datetime 
from math import ceil

breakIdx = 0
parentpath='YOUR PATH'
handle=sys.argv[1] #takes target twitter screenname as command-line argument
txtfilepath=parentpath+'/'+handle+'_tweet_dates.txt'
new_date = []

with open(jsonfilepath,'r') as fid:
      tweet = json.load(fid)
 
#authenticate
APP_KEY = #25 alphanumeric characters
APP_SECRET = #50 alphanumeric characters
twitter=Twython(APP_KEY,APP_SECRET,oauth_version=2) #simple authentication object
ACCESS_TOKEN=twitter.obtain_access_token()
twitter=Twython(APP_KEY,access_token=ACCESS_TOKEN)
 
#adapted from http://www.craigaddyman.com/mining-all-tweets-with-python/
#user_timeline=twitter.get_user_timeline(screen_name=handle,count=200) #if doing 200 or less, just do this one line
user_timeline=twitter.get_user_timeline(screen_name=handle,count=1) #get most recent tweet
lis=user_timeline[0]['id']-1 #tweet id # for most recent tweet
#time.sleep(60)
incremental = twitter.get_user_timeline(screen_name=handle,
      count = 200, include_retweets = True, max_id=lis)
user_timeline.extend(incremental)
lis = user_timeline[-1]['id']-1
date = user_timeline[-1]['created_at'].encode('ascii','ignore').decode("utf-8") 
date = datetime.datetime.strptime(date.strip(),"%a %b %d %H:%M:%S +0000 %Y")

# read the dates from previous file
date_old = []
tweet_old = []
for i,d in enumerate(tweet['date']):
      dummydate = datetime.datetime.strptime(d.strip(),"%a %b %d %H:%M:%S +0000 %Y")
      if dummydate<date:
            date_old.append(d)
            tweet_old.append(tweet['text'][i])

for d in reversed(user_timeline):
      date_old.append(d['created_at'].encode('ascii','ignore'))     
      tweet_old.append(d['text'].encode('ascii','ignore'))     

tweet = {'date':date_old,'text':tweet_old}
with open(txtfilepath,'w') as fid:
      for d in date_old:
            fid.write(d)
            fid.write("\n")
            
with open(jsonfilepath,'w') as fid:
      json.dump(tweet,fid)            

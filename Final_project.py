
#pip any library you need if you don't have it on your pc.
import tweepy
import twitter
import json
import tweepy
import csv
import pandas as pd
consumer_key = 'DiIsBWy1EsatoOWKpXnM5pOx8' # your key and secret here
consumer_secret = 'mc0qsu9pVFcHaOGDBGZBDTB80LhOBDfFSbMdEspDWIVgLLTtZg'
access_token = '920748428807716864-1HJE6frWop2LPemyj8W3LMD57uWSEJn'
access_token_secret = 'WvbHc3sIugEqDSpxT2YbnAdtdM7Jq7W0M986C9Bst5P7l'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
"""
for i in api.user_timeline(screen_name = 'realDonaldTrump',since = '2019-10-25',count = 10):
    print(i.text)
"""
rows = ['date','content']
with open('#MidwayMovie.csv','a') as f: #change the file name as movies name
    ### I made a mistake here for some moive names, some whith a extra space at the begining, some not.###

    c = csv.writer(f, delimiter=',', lineterminator='\n')
    c.writerow(rows)                        ##### pay attern about the space before #, I think I made mistake on this.
    for tweet in tweepy.Cursor(api.search,q="#MidwayMovie", lang="en",#q is hashtag, search youself on twitter that
                               # a movie's hashtag is
                               # then change q as that hashtag
                               since="2019-11-11",until = '2019-11-12').items():
        "next data for DS is 117-118"
        "next data for ternimate is 116-117"
        "midway enxt is 12-13"
        #change the since and unitl accordingly but day by day,
        #otherwise the request will stop.
        """
        after every run, have a rest for about 10-15mins, then change the date and run again."""
        print(tweet.created_at, tweet.text)
        c.writerow ([tweet.created_at, tweet.text])
f.close()

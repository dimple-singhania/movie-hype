import tweepy
import csv

api_key = '***********'  # your key and secret here
api_secret_key = '***********'
access_token = '***********'
access_token_secret = '***********'

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

rows = ['date', 'content']
with open('Irishman_TEST.csv', 'a') as f:  # change the file name as movies name

    c = csv.writer(f, delimiter=',', lineterminator='\n')
    c.writerow(rows)
    for tweet in tweepy.Cursor(api.search, q="#TheIrishman", lang="en", # CHANGE THE HASTAG FOR MOVIES HERE
                               since="2019-11-20", until='2019-11-21',  # CHANGE THE DATES HERE
                               tweet_mode='extended').items():
        # change the since and unitl accordingly but day by day,
        # otherwise the request will stop.

        # print(tweet.created_at, tweet.text)
        try:
            content = tweet.full_text
        except AttributeError:
            content = tweet.text
        c.writerow([tweet.created_at, content])
f.close()

# Need to remove duplicate rows

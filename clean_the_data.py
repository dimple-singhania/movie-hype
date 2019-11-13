from collections import defaultdict
import tweepy
import twitter
import json
import tweepy
import csv
import re
import pandas as pd
import emoji
from textblob import TextBlob
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
def extract_wild_text(file:str)->pd:
    ###this function extract all data out and made them into a dataframe for future use.
    frame = []
    #wild_text = []
    #time = []
    csvFile = open(file,'r')
    reader = csv.reader(csvFile)
    for item in reader:
        if reader.line_num == 1:
            pass
        else:
            time = (item[0])
            wild_text = (emoji.demojize(item[1]))#over here, I turn emoji into text, but we can also delete emoji
                                                    # becasue I think emoji may have emotions too,
                                                    #so I transfer them into text see if there any result.
            frame.append([time,wild_text])
    df = pd.DataFrame(frame,columns=['time','content'])
    return df
def clean_text(wild_text:list)->dict:
    #returns all cleaned text with only text, and how many times they appear.
    #also clean the stopwordss, but this one only makes for word count etc. not for future use.
    moviedict = defaultdict(lambda: 0)
    for tweet in wild_text.content:
        if 'RT' in tweet:# "but I love it  RT@SASX THIS move is bad" ->>"but I love it"
                                #"RT@SASX THIS move is bad  -->> RT@SASX THIS move is bad"
            if tweet.index('RT') > 5:
                tweet = tweet[:tweet.index('RT')]
            else:
                tweet = tweet[2:]
        tweet = ' '.join(re.sub("(@\w+)|([^A-Za-z]+)|(\w+:\/\/\S+)", " ", tweet).split())
        moviedict[tweet]+=1
        #moviedict[emoji.demojize(item[1])] +=1 #use emoji library to turn emoji into text, so that we could analyze it.
    return moviedict
def cleaninto_df(frame:pd) -> pd:
    #this one cleans the data, stop words and return words into root word by lemmatizer, and make a new column for the data frame.
    stop = stopwords.words('english')
    newStopWords = ['get', 'http','there','and','i','t','it','d']
    stop.extend(newStopWords)
    lemmatizer = WordNetLemmatizer()
    # this function cleans the data by REGX and store into a df.
    clean = []
    new_col=[]
    frame['Cleaned'] = None
    for tweet in frame.content:
        if 'RT' in tweet:
            if tweet.index('RT')>5:
                tweet = tweet[:tweet.index('RT')]
            else:
                tweet = tweet[2:]
        tweet = ' '.join(re.sub("(@\w+)|([^A-Za-z]+)|(\w+:\/\/\S+)", " ", tweet).split())
        clean.append(tweet.lower())
    for clean_tweet in clean:
        tokens = clean_tweet.split()
        clean_tokens = []
        for token in tokens:
            if token not in stop:
                clean_tokens.append(token)
        stems = []
        for item in clean_tokens:
            stems.append(lemmatizer.lemmatize(item))
        newword = ''
        for item in stems:
            newword += item + ' '  # if not + '', it will become: ILOVEYOUANDYOUDONTLOVEME. but should be: I LOVE YOU AND YOU DONT LOVE ME
            # print(newword)
        new_col.append(newword.lower())
    frame['Cleaned'] = new_col
    return frame
def sentiment(frame:pd) -> pd:
    #analyze all the sentiment for each sentence.
    Sentiment_polarity = []
    Sentiment_subjectivity = []
    frame['Sentiment_polarity','Sentiment_subjectivity'] = None
    for tweet in frame.Cleaned:
        blob = TextBlob(tweet)
        Sentiment_polarity.append(blob.sentiment.polarity)
        Sentiment_subjectivity.append(blob.sentiment.subjectivity)
    #print(len(Sentiment_polarity))
    frame['Sentiment_polarity'] = Sentiment_polarity
    frame['Sentiment_subjectivity'] = Sentiment_subjectivity
    return frame
#def write_file(frame:pd)->None:


def total__avg_polarity(frame:pd)->float:
    # these 2 function give the general sentiment for each file/each movie, so do not add it into the dataframe.
    return frame.Sentiment_polarity.sum()/frame.shape[0]
def total__avg_subjectivity(frame:pd)->float:
    return frame.Sentiment_subjectivity.sum()/frame.shape[0]




if __name__ == "__main__":
    ##feel free to call any functions you like and remeeber tochange the csv file name.
    tweets = extract_wild_text('#DoctorSleep.csv')###### input your datafile name    ########
                                                #######      #######
    #print(tweets)
    #clean = clean_text(tweets)
    clean = cleaninto_df(tweets)
    #print(cleaninto_df(tweets))
    total_sentiment = sentiment(clean)
    #polar = total__avg_polarity(total_sentiment)
    #sub = total__avg_subjectivity(total_sentiment)
    #print(total_sentiment.head)
    ### after get all info into the data frame, we save it into the csv for future use.#####
    total_sentiment.to_csv("#DoctorSleep_cleaned.csv")  ################# change this file name to XXX_leaned.csv############
                                             ################# change this file name to XXX_leaned.csv############
    print('done')

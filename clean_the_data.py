import csv
import re
import pandas as pd
import emoji
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def extract_wild_text(file:str)->pd:
    frame = []
    csvFile = open(file, 'r')
    reader = csv.reader(csvFile)
    for item in reader:
        if reader.line_num == 1:
            pass
        else:
            time = (item[0])
            wild_text = (emoji.demojize(item[1]))   # over here, I turn emoji into text, but we can also delete emoji
                                                    # becasue I think emoji may have emotions too,
                                                    # so I transfer them into text see if there any result.
            frame.append([time, wild_text])
    df = pd.DataFrame(frame, columns=['time', 'content'])
    return df


def cleaninto_df(frame:pd) -> pd:
    """
    this function cleans the data by REGX and store into a df.
    :param frame:
    :return:
    """
    # remove repeated characters EXAMPLE: DIMPLLLLEEEEE -> DIMPLE
    # nopunc = word_tokenize(nopunc) this might not work. find something else

    stop = stopwords.words('english')
    newStopWords = ['get', 'http','there','and','i','t','it','d']
    stop.extend(newStopWords)
    lemmatizer = WordNetLemmatizer()
    clean = []
    new_col = []
    frame['Cleaned'] = None
    for tweet in frame.content:
        if 'RT' in tweet:
            if tweet.index('RT')>5:
                tweet = tweet[:tweet.index('RT')]
            else:
                tweet = tweet[2:]
        # WHAT ARE WE TRYING TO CLEAN HERE?
        # cleaning with preprocessor library https://pypi.org/project/tweet-preprocessor/
        tweet = ' '.join(re.sub("(@\w+)|([^A-Za-z]+)|(\w+:\/\/\S+)", " ", tweet).split())
        # changes  #November1 -> November: need to remove full hashtag?
        # changes  @poetweatherford: -> poetweatherford
        # changes  don’t -> don t, children's -> children s
        print("after regex:" + str(tweet))
        clean.append(tweet.lower())
    for clean_tweet in clean:
        word_tokens = word_tokenize(clean_tweet)
        clean_tokens = [word for word in word_tokens if word not in stop]
        stems = []
        for item in clean_tokens:
            stems.append(lemmatizer.lemmatize(item))
        new_sentence = ' '.join(stems)
        new_col.append(new_sentence.lower())
    frame['Cleaned'] = new_col
    return frame


def sentiment(frame:pd) -> pd:
    Sentiment_polarity = []
    Sentiment_subjectivity = []
    for tweet in frame.Cleaned:
        blob = TextBlob(tweet)
        Sentiment_polarity.append(blob.sentiment.polarity)
        Sentiment_subjectivity.append(blob.sentiment.subjectivity)
    frame['Sentiment_polarity'] = Sentiment_polarity
    frame['Sentiment_subjectivity'] = Sentiment_subjectivity
    return frame


def total__avg_polarity(frame:pd) -> float:
    return frame.Sentiment_polarity.sum()/frame.shape[0]


def total__avg_subjectivity(frame:pd) -> float:
    return frame.Sentiment_subjectivity.sum()/frame.shape[0]


if __name__ == "__main__":
    # CHANGE THE INPUT CSV FILE HERE
    tweets = extract_wild_text('Harriet.csv')
    clean = cleaninto_df(tweets)
    total_sentiment = sentiment(clean)

    # WRITE THE NAME OF OUTPUT FILE HERE. MAKE IT F=DIFFERENT THAN THE INPUT FILE
    total_sentiment.to_csv("Harriet_test_cleaned_3.csv", index=False)
    print('DONE')

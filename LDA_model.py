
from textblob import TextBlob
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pandas as pd
import lda
def dic_cor(frame1:pd,frame2:pd)->None:
    #create dictionary and corpus
    integrate = []
    move1 = []
    move2 = []
    for tweet in frame1:
        spli = str(tweet).split()
        for letter in spli:
            move1.append(letter)
    for tweet in frame2:
        spli = str(tweet).split()
        for letter in spli:
            move2.append(letter)
    bigram = gensim.models.phrases.Phrases([move1], min_count=10, threshold=100)
    trigram = gensim.models.phrases.Phrases(bigram[move1], threshold=100)
    integrate.append(trigram[bigram[move1]])
    bigram = gensim.models.phrases.Phrases([move2], min_count=10, threshold=100)
    trigram = gensim.models.phrases.Phrases(bigram[move2], threshold=100)
    integrate.append(trigram[bigram[move2]])

    id2word = corpora.Dictionary(integrate)
    texts = integrate
    #return id2word
    #frequency dict###
    corpus = [id2word.doc2bow(text) for text in integrate]
    return id2word,corpus
def LDA_model(id2word:pd,corpus:pd)->list:
    # this function build the model and train it
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=5,
                                                random_state=100,
                                                update_every=0,
                                                iterations=50,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
    topics = lda_model.show_topics(num_words = 10)
    for topic in topics:
        print(topic)
    return lda_model
    """
    integrate = []
    for tweet in Mal_Cleaned:
        spli = str(tweet).split()
        for letter in spli:
            integrate.append(letter)
    bow = id2word.doc2bow(integrate)
    print("get_document_topics", lda_model.get_document_topics(bow))
    """
def document_topic(movie_list:list)->pd:
    # by having the result from the model, we could see a specific movie's topic here.
    for movie in movie_list:
        integrate = []
        for tweet in movie:
            spli = str(tweet).split()
            for letter in spli:
                integrate.append(letter)
        bow = id2word.doc2bow(integrate)
        print("get_document_topics for ", total_model.get_document_topics(bow))

    #get_document_topics =
if __name__ == "__main__":
    open_mal = pd.read_csv('Mal_cleaned.csv', error_bad_lines=False)
    Mal_Cleaned = open_mal.Cleaned
    open_ter = pd.read_csv('Terminator_cleaned.csv', error_bad_lines=False)
    Terminator_cleaned  = open_ter.Cleaned
    #print(Mal_Cleaned)
    id2word, corpus = dic_cor(Mal_Cleaned,Terminator_cleaned)#add movie cleaned file into it, and change the function set.#
    total_model = LDA_model(id2word,corpus)
    print(total_model)
    movie_list = [Mal_Cleaned,Terminator_cleaned]
    document_topic(movie_list)

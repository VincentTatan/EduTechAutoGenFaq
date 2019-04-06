import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def topic_extraction(df):
    # Importing necessary model values
    # Getting the X_train
    X_train = df.title

    # tokenize and vectorize the words inside the list of documents/tweets
    vectorizer = CountVectorizer(stop_words='english')
    X_train_dtm = vectorizer.fit_transform(X_train)
    vocab = np.array(vectorizer.get_feature_names())

    # Using sklearn library to get the necessary LDA model
    from sklearn import decomposition

    num_topics = 5
    num_top_words = 5
    clf = decomposition.NMF(n_components=num_topics, random_state=1)

    # this next step may take some time to train depending on the texts you have
    doctopic = clf.fit_transform(X_train_dtm)
    doctopic.shape

    # Getting the dominant topic for each word
    topic_words = []

    # Appending top important vocabset list onto topic_words list
    for topic in clf.components_:
        #     npargsort gets the index based on the order, [::-1] order it descending and finally num_top_words will filter it
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        topic_words.append([vocab[i] for i in word_idx])


    # Making DataFrame that gets the doctopic (values of topics for each text)
    dftopic = pd.DataFrame(doctopic, columns=topic_words)
    dftopicinv = dftopic.T

    # Getting the dominant topic
    topic_series = []
    for i in np.arange(dftopic.shape[0]):
        topic_series.append(dftopicinv[i].argmax())

    dftopic['dominanttopic'] = topic_series
    df['dominanttopic'] = topic_series

    return df

def create_dict_list_of_topics(df):
    # Create a list of dict based on tickers and labels
    dictlist = []
    unique_list = df.dominanttopic.unique()
    for dominanttopic in unique_list:
        dominant_topic_string = ",".join(dominanttopic)
        dictlist.append({'value': dominant_topic_string, 'label': dominant_topic_string})
    print(dictlist)
    return dictlist
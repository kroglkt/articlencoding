from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaModel
from gensim.models import CoherenceModel
from sklearn.model_selection import train_test_split
import os, re
import pickle

with open('../function_words/funktionsord.txt', 'r', encoding='utf-8') as f:
    stop_words = f.readlines()
    stop_words = [x.replace('\n','') for x in stop_words]

def split_words(text):
    '''Returns an array with text split into words'''
    text = text.lower()
    string = np.array(text.split(), dtype=str)
    no_dot = np.array([remove_dots(x) for x in string])
    return np.array(list(filter(None, no_dot)))

def remove_symbols(text):
    return re.sub('\W+',' ', text)

def remove_dots(word):
    return re.sub(r',|\.|:|!|\?|;', '', word)

def tokenize_docs_for_lda(corpus):
    docs = [remove_symbols(x) for x in corpus]
    docs = [split_words(x.lower().strip()) for x in docs]
    docs = [[token for token in doc if not token.isnumeric()] for doc in docs]
    print("Halfway there...")
    docs = [[token for token in doc if len(token)>1] for doc in docs]
    docs = [[token for token in doc if token not in stop_words] for doc in docs]
    return docs

def load_corpus():
    print("Loading corpus...")
    path = '../data/additional/scraped'
    files = os.listdir(path)
    dataframes = []
    for file in files:
        dataframes.append(pd.read_json(path+'/'+file))

    dataframe = pd.concat(dataframes)
    del dataframe['level_0']
    del dataframe['index']

    print("Loaded!")
    return dataframe

def create_lda_dictionary(docs):
    dictionary = Dictionary(docs)
    #Remove words that occur in less than 20 documents and more than 10% of all documents
    dictionary.filter_extremes(no_below=20, no_above=0.1)
    print("Creating dictionary...")
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    print("Number of unique tokens:", len(dictionary))
    print("Number of documents:", len(corpus))
    return dictionary, corpus


def main():
    data = load_corpus()
    bodies = list(data["Body"])
    authors = list(data["Byline"])

    train_X, test_X, train_y, test_y = train_test_split(bodies, authors, test_size=0.2,
                                                        random_state=42, stratify=authors)

    print("Tokenizing...")
    docs = tokenize_docs_for_lda(train_X)
    print("Tokenized!")

    dictionary, corpus = create_lda_dictionary(docs)
    assert len(dictionary) > 0, "Oh no! No unique words... You need more text!"


    num_topics = list(range(20,30))
    num_keywords = len(num_topics)

    LDA_models = {}
    LDA_topics = {}

    coherences = []

    _ = dictionary[0]

    for i in num_topics:
        print("Training model with num topic", i)
        id2word = dictionary.id2token
        model = LdaModel(corpus=corpus,
                        id2word=id2word,
                        chunksize=2000,
                        alpha='auto',
                        eta='auto',
                        iterations=400, #400
                        num_topics=i,
                        passes=20, #20
                        minimum_probability=0.0,
                        eval_every=5)

        coherence_model = CoherenceModel(
            model = model, texts=docs, dictionary=dictionary, coherence='c_v')

        coherence = coherence_model.get_coherence()
        coherences.append((i, coherence))

    print(coherences)
    x = [x[1] for x in coherences]
    topics = [x[0] for x in coherences]
    plt.plot(topics, x)
    plt.show()

    with open("coherences.dat", 'wb') as f:
        pickle.dump(coherences, f)

if __name__ == '__main__':
    var = main()

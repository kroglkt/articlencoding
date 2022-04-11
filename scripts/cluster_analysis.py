from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaModel
from gensim.models import CoherenceModel
from sklearn.model_selection import train_test_split
import os, re

#Courtesy to user12446118 on StackOverflow :-)

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

def jaccard_similarity(topic_1, topic_2):
    intersection = set(topic_1).intersection(set(topic_2))
    union = set(topic_1).union(set(topic_2))
                    
    return float(len(intersection))/float(len(union))

def main():
    data = load_corpus()
    bodies = list(data["Body"])
    authors = list(data["Byline"])

    train_X, test_X, train_y, test_y = train_test_split(bodies, authors, test_size=0.2,
                                                        random_state=42, stratify=authors)

    print("Tokenizing...")
    corpus = tokenize_docs_for_lda(train_X)
    print("Tokenized!")

    dirichlet_dict = Dictionary(corpus)
    bow_corpus = [dirichlet_dict.doc2bow(text) for text in corpus]

    num_topics = list(range(8,20))
    num_keywords = len(num_topics)

    LDA_models = {}
    LDA_topics = {}

    coherences = []

    for i in num_topics:
        print("Training model with num topic", i)
        LDA_model = LdaModel(corpus=bow_corpus,
                                 id2word=dirichlet_dict,
                                 num_topics=i,
                                 update_every=1,
                                 chunksize=len(bow_corpus),
                                 passes=20,
                                 alpha='auto',
                                 random_state=42)

        coherence_model = CoherenceModel(
            model = LDA_model, texts=corpus, dictionary=dirichlet_dict, coherence='c_v')

        coherence = coherence_model.get_coherence()
        coherences.append((i, coherence))

    print(coherences)

if __name__ == '__main__':
    main()

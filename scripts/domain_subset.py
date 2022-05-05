import pandas as pd
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
import os

def load_data():
    path = '../data/additional/scraped'
    files = os.listdir(path)
    dataframes = []
    for file in tqdm(files):
        dataframes.append(pd.read_json(path+'/'+file))

    dataframe = pd.concat(dataframes)
    del dataframe['level_0']
    del dataframe['index']

    return dataframe

data = load_data()
domains = data.Domain.value_counts()
domains1000 = domains[domains>=1000]
domains1000_list = list(domains1000.index)

del domains1000_list[domains1000_list.index('bold.dk')]

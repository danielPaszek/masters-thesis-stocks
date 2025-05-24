from headers import *
import pandas as pd
import numpy as np
import random

def custom_train_test_split(paths=['../data/combined_inner_ticker.csv']):
    dfs = []
    for path in paths:
        dfs.append(pd.read_csv(path))
    df = pd.concat(dfs, ignore_index=True)
    df['to_join_id'] = df.index

    companies = df['ticker'].unique().tolist()
    k = int(0.2 * len(companies))
    random.seed(2)
    random_values = random.sample(range(0, len(companies) + 1), k)
    test_companies = [companies[i] for i in random_values]

    testData = df[df['ticker'].isin(test_companies)]
    trainData = df[~df['ticker'].isin(test_companies)]
    return trainData, testData

# custom_train_test_split(['../data/combined_inner_ticker.csv', '../data/extra-data/combined_inner_ticker.csv'])

# TODO!!!!!!!!!! final-data-relative has 466 companies, not 500! WHAT HAPPENED???????????????
# ANSWER: THOSE ARE BANKS/FINANCIAL INSTITUTIONS lost because of dropna().
# TODO: Info w magisterce, że wykluczono instytucje finansowe i banki
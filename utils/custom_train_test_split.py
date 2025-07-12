from headers import *
import pandas as pd
import numpy as np
import random

def joinDfs(paths):
    dfs = []
    for path in paths:
        dfs.append(pd.read_csv(path))
    df = pd.concat(dfs, ignore_index=True)
    df['to_join_id'] = df.index
    return df

# Compute "heavy" since we do 30-40k conversions to datetime
def per_year_train_test_split(paths=['../data/combined_inner_ticker.csv'], splitDate='30-06-2021', format='%m-%Y'):
    splitDate = pd.to_datetime(splitDate, format='%d-%m-%Y')
    df = joinDfs(paths)
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x, format=format))
    trainData = df[df['date'] <= splitDate]
    testData = df[df['date'] > splitDate]
    return trainData, testData

def custom_train_test_split(paths=['../data/combined_inner_ticker.csv']):
    df = joinDfs(paths)
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

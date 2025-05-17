from joblib import dump, load
import pandas as pd
from headers import *

# TODO: ALL MODELS RETURN 1 FOR ALL OF THE DATA THAT WAS GIVEN TO THEM!!!!
for label in yAlpha:
    model = load('../data/svm_models/' + label + '.joblib')
    testedData = pd.read_csv('../data/svm_results/' + label + '.csv')

    X = testedData[ratioKeys + relativeRatioKeys]
    y = testedData[label]
    df = pd.read_csv('../data/combined_inner.csv')

    print(f'data count: {testedData[label].count()}')
    print(f'data mean: {testedData[label].mean()}')

    print('====TEST=====')
    y_pred = model.predict(X)
    xTaken = X[y_pred == 1]
    results = testedData.loc[testedData.index.intersection(xTaken.index)]

    print(f'res count {results[label].count()}')
    print(f'res count {results[label].mean()}')

    print(f'diff: {results[label].mean() - testedData[label].mean()}')
    print('-------------------------------------------------')


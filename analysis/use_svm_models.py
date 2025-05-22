from joblib import dump, load
import pandas as pd
import numpy as np
from headers import *
from sklearn.metrics import classification_report, make_scorer, confusion_matrix

for label in yAlpha:
    model = load('./models2/' + label + '.joblib')
    testedData = pd.read_csv('../data/svm_results/' + label + '.csv')

    X = testedData[ratioKeys + relativeRatioKeys]
    # TODO: adjust/test cut off
    y = np.where(testedData[label] <= 0, 0, 1)
    df = pd.read_csv('../data/combined_inner.csv')

    print(f'data count: {testedData[label].count()}')
    print(f'data mean: {testedData[label].mean()}')

    print('====TEST=====')
    y_pred = model.predict(X)
    xTaken = X[y_pred == 1]
    results = testedData.loc[testedData.index.intersection(xTaken.index)]

    print(f'res count {results[label].count()}')
    print(f'res mean {results[label].mean()}')

    print(confusion_matrix(y, y_pred))

    print(f'diff: {results[label].mean() - testedData[label].mean()}')
    print('-------------------------------------------------')


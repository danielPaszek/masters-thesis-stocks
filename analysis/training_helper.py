from headers import *
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt


def drawFrom1results(toPlot, yLabel, x, title='', keys=['svc', 'tree', ]):
    if len(keys) <= 3:
        fig, axes = plt.subplots(ncols=len(keys), figsize=(16, 4))
    else:
        fig, axes = plt.subplots(ncols=int((len(keys)+1)/2), nrows=2, figsize=(20, 10))
        axes = axes.flatten()

    for i, key in enumerate(keys):
        axes[i].plot(x, [d['mean'] for d in toPlot[key]], color='red', label='mean')
        axes[i].plot(x, [d['median'] for d in toPlot[key]], color='green', label='median')

        axes[i].legend(loc='upper left')
        axes[i].grid(True)
        axes[i].set_xscale('log')
        axes[i].set_title(f'{yLabel} {key} {title}')
        axes[i].set_xlabel('Cutoff')
        axes[i].set_ylabel('Alpha')


        if toPlot[key][0]['taken'] != -1:
            ax1b = axes[i].twinx()
            ax1b.plot(x, [d['taken'] for d in toPlot[key]], color='blue', label='taken')
            ax1b.legend(loc='upper right')
            ax1b.set_yscale('log')

def getPipeline(isBalanced):
    if isBalanced:
        return {
            'tree': Pipeline([
                ('scaler', StandardScaler()),
                ('tree', DecisionTreeClassifier(class_weight='balanced'))
            ]),
            'svc': Pipeline([
                ('scaler', StandardScaler()),
                ('svc', LinearSVC(class_weight='balanced'))
            ])
        }
    return {
        'tree': Pipeline([
            ('scaler', StandardScaler()),
            ('tree', DecisionTreeClassifier())
        ]),
        'svc': Pipeline([
            ('scaler', StandardScaler()),
            ('svc', LinearSVC())
        ])
    }

def trainPipeline(cutoffs, yLabels, trainDf, testDf, thresholds, isBalanced=False):
    X_train = trainDf[ratioKeys + relativeRatioKeys]
    X_test = testDf[ratioKeys + relativeRatioKeys]
    resultsToPlot = {}
    for yLabel in yLabels:
        if yLabel not in resultsToPlot:
            resultsToPlot[yLabel] = {}
        for cutoff in cutoffs:
            y_train = np.where(trainDf[yLabel] <= cutoff, 0, 1)
            y_test = np.where(testDf[yLabel] <= cutoff, 0, 1)
            pipelines = getPipeline(isBalanced)
            params = [
                {
                    'tree__criterion': ["gini", "entropy", "log_loss"],
                },
                {
                    'svc__C': [0.1, 0.5, 1.0, 5.0, 10.0],
                    'svc__penalty': ['l1', 'l2']
                }
            ]
            resultsToPlot = cvPipeline(X_test, X_train, cutoff, params, pipelines, resultsToPlot, testDf, yLabel, y_test, y_train, thresholds)

    return resultsToPlot


def cvPipeline(X_test, X_train, cutoff, params, pipelines, resultsToPlot, testDf, yLabel, y_test, y_train, thresholds):
    xTrue = X_test[y_test == 1]
    trueData = testDf.loc[testDf.index.intersection(xTrue.index)]
    print('-----------------')
    print(
        f'% of True in dataset {round(len(y_test[y_test == 1]) / len(y_test) * 100, 2)}% resulted in {round(trueData.loc[:, yLabel].mean() * 100, 2)}% and median {round(trueData.loc[:, yLabel].median() * 100, 2)}%')

    for (key, pipeline), param_grid in zip(pipelines.items(), params):
        grid = GridSearchCV(pipeline,
                            param_grid,
                            cv=StratifiedKFold(3, shuffle=True, random_state=3),
                            refit=True,
                            n_jobs=-1,
                            # scoring='f1',
                            )
        grid.fit(X_train, y_train)
        y_pred = grid.predict(X_test)

        wholeTestData = testDf.loc[testDf.index.intersection(X_test.index)]

        xTaken = X_test[y_pred == 1]

        takenData = testDf.loc[testDf.index.intersection(xTaken.index)]

        prc = round(takenData.loc[:, yLabel].count() / wholeTestData.loc[:, yLabel].count(), 4) * 100

        print(f'MODEL {key}')
        print(f'For {yLabel}, yCutoff = {cutoff}, taken used - {takenData.loc[:, yLabel].count()} is {prc}%')
        print(
            f'Mean was {round(takenData.loc[:, yLabel].mean() * 100, 2)}%, median was {round(takenData.loc[:, yLabel].median() * 100, 2)}%')


        if key not in resultsToPlot[yLabel]:
            resultsToPlot[yLabel][key] = []
        resultsToPlot[yLabel][key].append({
            'mean': takenData.loc[:, yLabel].mean(),
            'median': takenData.loc[:, yLabel].median(),
            'taken': takenData.loc[:, yLabel].count()
        })
        # run pipeline by hand to use decision function
        if key == 'svc':
            model = grid.best_estimator_['svc']
            scaler = grid.best_estimator_['scaler']
            X_scaled = scaler.transform(X_test)
            scores = model.decision_function(X_scaled)
            for threshold in thresholds:
                barrier = np.percentile(scores, threshold)
                y_pred_threshold = scores >= barrier
                xTakenThreshold = X_test[y_pred_threshold]
                takenDataThreshold = testDf.loc[testDf.index.intersection(xTakenThreshold.index)]
                print(f'% of True taken with threshold {threshold} adjustment -  {takenDataThreshold.loc[:, yLabel].count()}')
                print(
                    f'For threshold data - mean was {round(takenDataThreshold.loc[:, yLabel].mean() * 100, 2)}%, median was {round(takenDataThreshold.loc[:, yLabel].median() * 100, 2)}%')
                thresholdLabel = f'svcThreshold{threshold}'
                if thresholdLabel not in resultsToPlot[yLabel]:
                    resultsToPlot[yLabel][thresholdLabel] = []
                resultsToPlot[yLabel][thresholdLabel].append({
                    'mean': takenDataThreshold.loc[:, yLabel].mean(),
                    'median': takenDataThreshold.loc[:, yLabel].median(),
                    'taken': -1
                })
    print('-----------------')
    return resultsToPlot

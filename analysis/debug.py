cutoffs = [0.0, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20, 0.25, 0.35]

trainDf, testDf = custom_train_test_split(
    ['../data/combined_inner_ticker.csv', '../data/extra-data/combined_inner_ticker.csv'])
X_train = trainDf[ratioKeys + relativeRatioKeys]
X_test = testDf[ratioKeys + relativeRatioKeys]

# TODO: Czy dobór cutoff jest błędem na zbiorze testowym?? Czy nie powinienem mieć walidacyjnego?

resultsToPlotNoWeights = {}
thresholds = [70, 80, 90]

for yLabel in yAlpha:
    if yLabel not in resultsToPlotNoWeights:
        resultsToPlotNoWeights[yLabel] = {}
    for cutoff in cutoffs:
        y_train = np.where(trainDf[yLabel] <= cutoff, 0, 1)
        y_test = np.where(testDf[yLabel] <= cutoff, 0, 1)
        pipelines = {
            'tree': Pipeline([
                ('scaler', StandardScaler()),
                ('tree', DecisionTreeClassifier())
            ]),
            'svc': Pipeline([
                ('scaler', StandardScaler()),
                ('svc', LinearSVC())
            ])
        }
        params = [
            {
                'tree__criterion': ["gini", "entropy", "log_loss"],
            },
            {
                'svc__C': [0.1, 0.5, 1.0, 5.0, 10.0],
                'svc__penalty': ['l1', 'l2']
            }
        ]
        for (key, pipeline), param_grid in zip(pipelines.items(), params):
            grid = GridSearchCV(pipeline,
                                param_grid,
                                cv=StratifiedKFold(3, shuffle=True, random_state=3),
                                verbose=1,
                                refit=True,
                                n_jobs=-1,
                                # scoring='f1',
                                )
            grid.fit(X_train, y_train)
            y_pred = grid.predict(X_test)

            wholeTestData = testDf.loc[testDf.index.intersection(X_test.index)]

            xTaken = X_test[y_pred == 1]
            xTrue = X_test[y_test == 1]

            takenData = testDf.loc[testDf.index.intersection(xTaken.index)]
            trueData = testDf.loc[testDf.index.intersection(xTrue.index)]

            prc = round(takenData.loc[:, yLabel].count() / wholeTestData.loc[:, yLabel].count(), 4) * 100
            print(f'MODEL {key}')
            print(f'For {yLabel}, yCutoff = {cutoff}, taken used - {takenData.loc[:, yLabel].count()} is {prc}%')
            print(
                f'Mean was {round(takenData.loc[:, yLabel].mean() * 100, 2)}%, median was {round(takenData.loc[:, yLabel].median() * 100, 2)}%')

            print(
                f'% of True in dataset {round(len(y_test[y_test == 1]) / len(y_test) * 100, 2)}% resulted in {round(trueData.loc[:, yLabel].mean() * 100, 2)}% and median {round(trueData.loc[:, yLabel].median() * 100, 2)}%')

            # run pipeline by hand to use decision function
            if key == 'svc':
                model = grid.best_estimator_['svc']
                scaler = grid.best_estimator_['scaler']
                X_scaled = scaler.transform(X_test)
                scores = model.decision_function(X_scaled)
                for threshold in thresholds:
                    threshold = np.percentile(scores, 80)
                    y_pred_threshold = scores >= threshold
                    xTakenThreshold = X_test[y_pred_threshold]
                    takenDataThreshold = testDf.loc[testDf.index.intersection(xTakenThreshold.index)]
                    print(f'% of True taken with threshold adjustment -  {takenDataThreshold.loc[:, yLabel].count()}')
                    print(
                        f'For threshold data - mean was {round(takenDataThreshold.loc[:, yLabel].mean() * 100, 2)}%, median was {round(takenDataThreshold.loc[:, yLabel].median() * 100, 2)}%')
            print('-----------------')

            if key not in resultsToPlotNoWeights[yLabel]:
                resultsToPlotNoWeights[yLabel][key] = []
            resultsToPlotNoWeights[yLabel][key].append({
                'mean': takenData.loc[:, yLabel].mean(),
                'median': takenData.loc[:, yLabel].median(),
                'taken': takenData.loc[:, yLabel].count()
            })
            if key == 'svc':
                if 'svcThreshold' not in resultsToPlotNoWeights[yLabel]:
                    resultsToPlotNoWeights[yLabel]['svcThreshold'] = []
                resultsToPlotNoWeights[yLabel]['svcThreshold'].append({
                    'mean': takenDataThreshold.loc[:, yLabel].mean(),
                    'median': takenDataThreshold.loc[:, yLabel].median(),
                    'taken': takenDataThreshold.loc[:, yLabel].count()
                })
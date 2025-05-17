import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, make_scorer
from sklearn.pipeline import Pipeline
from joblib import dump, load

ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales', 'evToGrossProfit', 'priceToGrossProfit']
yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
yAlpha = ['alpha1Year','adjustedAlpha1Year','equalAlpha1Year','equalAdjustedAlpha1Year','alpha2Year','adjustedAlpha2Year','equalAlpha2Year','equalAdjustedAlpha2Year']

numericalKeys = ratioKeys + yKeys + y2Keys
relativeRatioKeys = [x + '_relative' for x in ratioKeys]

df = pd.read_csv('../data/combined_inner.csv')
X = df[ratioKeys + relativeRatioKeys]

# #  https://stackoverflow.com/questions/48468115/how-to-create-a-customized-scoring-function-in-scikit-learn-for-scoring-a-set-of
# import sklearn.utils.multiclass
# def return_binary(y):
#     return "binary"
# sklearn.utils.multiclass.type_of_target = return_binary


# For loop with all the models is too slow. Run each training in separate run
# yLabel = 'alpha1Year'
# yLabel = 'adjustedAlpha1Year'
# yLabel = 'equalAlpha1Year'
# yLabel = 'equalAdjustedAlpha1Year'
# yLabel = 'alpha2Year'
# yLabel = 'adjustedAlpha2Year'
# yLabel = 'equalAlpha2Year'
# yLabel = 'equalAdjustedAlpha2Year'
for yLabel in yAlpha:
    yContinuous = df[yLabel]
    # TODO: adjust/test cut off
    y = np.where(yContinuous <= 0, 0, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('svc', SVC())
    ])
    # TODO: write in paper problem with loss/score function. confusion matrix and total return
    # TODO: workaround - adjust cut off
    # alphaScore = make_scorer(scoreAlpha)
    # param_grid = {
    #     'svc__C': [10],
    # }
    # TODO: SAVE MODEL PARAM. Not results, also test on 2015-2018 data, since they are not in training
    param_grid = {
        'svc__C': [0.1, 1, 10],
        'svc__gamma': ['scale', 'auto'],
        'svc__kernel': ['rbf', 'linear']
    }

    grid = GridSearchCV(pipeline, param_grid,
                        cv=3, verbose=2,
                        refit=True, n_jobs=-1
                        # scoring=alphaScore
                        )
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    xTaken = X_test[y_pred == 1]
    # TUTAJ JEST CHYBA BŁĄD - czy X_test ma ten sam indeks?
    # Chyba lepiej puścić jeszcze raz i dodać kolumne id i po niej joinować
    results = df.loc[df.index.intersection(xTaken.index)]
    results.to_csv('../data/svm_results/' + yLabel + '.csv', index=False)

    estimator = grid.best_estimator_
    dump(grid, '../data/svm_models/' + yLabel + '.joblib')

    print('Got mean of: ' + str(results.loc[:, yLabel].mean()))
    print("Best parameters:", grid.best_params_)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    # TODO: Do I train this for each y column?

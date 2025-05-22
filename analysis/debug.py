from joblib import dump, load
import pandas as pd
import numpy as np
from headers import *
from sklearn.metrics import classification_report, make_scorer, confusion_matrix
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from scipy import stats
import statsmodels.api as sm

for yLabel in yAlpha:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
    results = sm.OLS(y_train, X_train).fit()
    model = results.model
    model.predict()
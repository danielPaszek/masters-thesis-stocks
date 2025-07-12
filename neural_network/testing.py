# Test with combined_inner_ticker, but I think we can generate just absolute data and test it too. It is because we will have a series that will show past

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import TimeDistributed
import tensorflow as tf
import keras
from keras import optimizers
from keras.callbacks import History
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation, concatenate
import numpy as np
import pandas as pd
from headers import *
from utils.custom_train_test_split import custom_train_test_split, per_year_train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, MinMaxScaler



np.random.seed(10)

def transformToTimesteps(df, yLabel, timesteps, cutoff = 0.0):
    companies = pd.unique(df['ticker'])
    data = []
    y = []
    for company in companies:
        rows = df[df['ticker'] == company]
        # data.append([]) no need for another dimension
        for i in range(len(rows)-timesteps):
            curr = rows[i:i+timesteps]
            data.append(curr[ratioKeys + relativeRatioKeys].to_numpy())
            y.append(int(curr.iloc[-1, :][yLabel] > 0.0))

    return np.array(data), np.array(y)


series_length = 24
# TODO: create a new dataset with just ratio keys
features = len(relativeRatioKeys+ratioKeys)
# Maybe having company info won't be bad??
files = ['../data/deduplicated/combined_inner_ticker.csv']
yLabels = ['alpha1Year']


# trainDf, testDf = per_year_train_test_split(files, format='%Y-%m-%d')
trainDf, testDf = custom_train_test_split(files)
scaler = StandardScaler()
trainDf[ratioKeys + relativeRatioKeys + yAlpha] = scaler.fit_transform(trainDf[ratioKeys + relativeRatioKeys + yAlpha])
testDf[ratioKeys + relativeRatioKeys + yAlpha] = scaler.transform(testDf[ratioKeys + relativeRatioKeys + yAlpha])

for yLabel in yLabels:
    print('Starting')
    X_train, y_train = transformToTimesteps(trainDf, yLabel, series_length)
    X_test, y_test = transformToTimesteps(testDf, yLabel, series_length)
#     # TODO: Add dropout
    lstm_input = Input(shape=(series_length, features), name='lstm_input')
    inputs = LSTM(150)(lstm_input)
    output = Dense(1, activation='sigmoid')(inputs)
    model = Model(inputs=lstm_input, outputs=output)
    adam = optimizers.Adam()
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x=X_train, y=y_train, epochs=15, shuffle=True, validation_split=0.1)

    y_pred = model.predict(X_test)
    y_pred01 = (y_pred > 0.5).astype(int)

    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=1, return_dict=True)
    print("Scores - " + str(scores))
    print('====')
    print(classification_report(y_test, y_pred01))
    print('------')
    print(confusion_matrix(y_test, y_pred01))


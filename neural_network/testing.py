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
import itertools
from keras.callbacks import EarlyStopping




np.random.seed(10)

def transformToTimesteps(df, yLabel, timesteps, cutoff = 0.0):
    companies = pd.unique(df['ticker'])
    data = []
    y = []
    yPerc = []
    for company in companies:
        rows = df[df['ticker'] == company]
        # data.append([]) no need for another dimension
        for i in range(len(rows)-timesteps):
            curr = rows[i:i+timesteps]
            data.append(curr[ratioKeys].to_numpy())
            y.append(int(curr.iloc[-1, :][yLabel] > 0.0))
            yPerc.append(curr.iloc[-1, :][yLabel])

    return np.array(data), np.array(y), np.array(yPerc)

def createModel(dropout=0.0, seqDropout=0.0):
    lstm_input = Input(shape=(series_length, features), name='lstm_input')
    inputs = LSTM(150, dropout=dropout, recurrent_dropout=seqDropout)(lstm_input)
    output = Dense(1, activation='sigmoid')(inputs)
    model = Model(inputs=lstm_input, outputs=output)
    adam = optimizers.Adam()
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    return model


series_length = 24
features = len(ratioKeys)
files = ['../data/lstm/combined_whole_ticker.csv']
yLabels = ['alpha1Year']
dropouts = [0.0, 0.2, 0.4]
seqDropouts = [0.0, 0.2, 0.4]

# TODO: MOVE TO notebook
trainDf, testDf = per_year_train_test_split(files, splitDate='30-04-2020')
# trainDf, testDf = custom_train_test_split(files)
scaler = StandardScaler()
trainDf[ratioKeys + yAlpha] = scaler.fit_transform(trainDf[ratioKeys + yAlpha])
testDf[ratioKeys + yAlpha] = scaler.transform(testDf[ratioKeys + yAlpha])

for params in itertools.product(yLabels, dropouts, seqDropouts):
    yLabel, dropout, seqDropout = params
    print('==================')
    print(f'Starting label: {yLabel} and dropout: {dropout}, seq dropout: {seqDropout}')
    X_train, y_train, yPerc_train = transformToTimesteps(trainDf, yLabel, series_length)
    X_test, y_test, yPerc_test = transformToTimesteps(testDf, yLabel, series_length)
    model = createModel(dropout=dropout, seqDropout=seqDropout)
    model.fit(x=X_train, y=y_train, epochs=15, shuffle=True, validation_split=0.1)

    y_pred = model.predict(X_test)
    y_pred = y_pred.flatten()
    y_pred01 = (y_pred > 0.5).astype(int)

    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=1, return_dict=True)
    print("Scores - " + str(scores))
    print('====')
    print(classification_report(y_test, y_pred01))
    print('------')
    print(confusion_matrix(y_test, y_pred01))

    takenPerc = yPerc_test[y_pred01 == 1]
    prc = round(len(takenPerc) / len(yPerc_test) * 100, 2)
    print(f'Taken percent from dataset was {prc}%')
    print(f'Mean was {np.mean(takenPerc)} and median was {np.median(takenPerc)}')

# CHAT IMPROVEMENTS
# from keras.layers import BatchNormalization
# from keras.callbacks import EarlyStopping, ReduceLROnPlateau
#
#
# def createModel(dropout=0.0, seqDropout=0.0):
#     lstm_input = Input(shape=(series_length, features), name='lstm_input')
#
#     # First LSTM layer with batch normalization
#     x = LSTM(128, return_sequences=True,
#              dropout=dropout, recurrent_dropout=seqDropout)(lstm_input)
#     x = BatchNormalization()(x)
#
#     # Second LSTM layer
#     x = LSTM(64, dropout=dropout, recurrent_dropout=seqDropout)(x)
#     x = BatchNormalization()(x)
#
#     # Dense layers
#     x = Dense(32, activation='relu')(x)
#     x = Dropout(dropout)(x)
#     output = Dense(1, activation='sigmoid')(x)
#
#     model = Model(inputs=lstm_input, outputs=output)
#
#     # Use a lower learning rate
#     adam = optimizers.Adam(learning_rate=0.001)
#     model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
#     return model
#
#
# # Create callbacks for training
# early_stopping = EarlyStopping(
#     monitor='val_loss',
#     patience=5,
#     restore_best_weights=True
# )
#
# reduce_lr = ReduceLROnPlateau(
#     monitor='val_loss',
#     factor=0.2,
#     patience=3,
#     min_lr=0.00001
# )
#
# # During training, use the callbacks:
# model.fit(
#     x=X_train,
#     y=y_train,
#     epochs=50,
#     batch_size=32,
#     shuffle=True,
#     validation_split=0.1,
#     callbacks=[early_stopping, reduce_lr]
# )

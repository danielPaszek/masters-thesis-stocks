import pandas as pd
import json
from utils.mappingUtils import *
from datetime import datetime
import os

fileNames = os.listdir('./data/market-data')

for fileName in fileNames:
    with open('./data/market-data/' + fileName) as json_data:
        try:
            marketData = json.load(json_data)
            f = open('./data/transformed/' + fileName)
            transformedData = json.load(f)
        except:
            print('Error reading ' + fileName)
            with open('./data/error/' + fileName, 'w', encoding='utf-8') as f:
                f.write(json_data.read())
        dividends = marketData['dividends']
        cutoffDate = datetime.strptime('2015-01-01', '%Y-%m-%d')
        # record date but whatever
        latestDividends = [x for x in dividends if datetime.strptime(x['date'], '%Y-%m-%d') > cutoffDate]
        rollingTotal = {}
        currSum = 0
        for dividend in latestDividends:
            currSum += dividend['splitAdjAmount']
            # ex-date
            date = dividend.get('recordDate') if dividend.get('recordDate', 0) else dividend.get('date')
            rollingTotal[dividend['recordDate']] = currSum

        for year, yearData in transformedData.items():
            for month, montData in yearData.items():
                monthDate = datetime.strptime(montData['date'], '%Y-%m-%d')
                latestTotal = None
                for date, total in rollingTotal.items():
                    diff = monthDate - datetime.strptime(date, '%Y-%m-%d')
                    if (diff.days < 0):
                        break
                    latestTotal = total
                montData['adjustedTotalPrice'] = latestTotal + montData['price']

        break

import pandas as pd
import json
from utils.mappingUtils import *
from datetime import datetime
import os

# market-data & transformed -> results
fileNames = os.listdir('./data/extra-data/market-data')

for fileName in fileNames:
    with open('./data/extra-data/market-data/' + fileName) as json_data:
        try:
            marketData = json.load(json_data)
            f = open('./data/extra-data/transformed/' + fileName)
            transformedData = json.load(f)
        except:
            print('Error reading ' + fileName)
            with open('./data/extra-data/error/' + fileName, 'w', encoding='utf-8') as f:
                f.write(json_data.read())
        dividends = marketData['dividends']
        cutoffDate = datetime.strptime('2015-01-01', '%Y-%m-%d')
        # record date but whatever
        latestDividends = [x for x in dividends if datetime.strptime(x['date'], '%Y-%m-%d') > cutoffDate]
        rollingTotal = {}
        rollingTotalSpinoffExcl = {}
        currSum = 0
        currSumSpinoffExcl = 0
        for dividend in latestDividends:
            currSum += dividend['splitAdjAmount']
            # ex-date
            date = dividend.get('recordDate') if dividend.get('recordDate', 0) else dividend.get('date')

            if dividend['type'] != 'Spin-off':
                currSumSpinoffExcl += dividend['splitAdjAmount']
                rollingTotalSpinoffExcl[date] = currSumSpinoffExcl
            rollingTotal[date] = currSum

        for year, yearData in transformedData.items():
            for month, monthData in yearData.items():
                monthDate = datetime.strptime(monthData['date'], '%Y-%m-%d')
                latestTotal = 0
                latestTotalSpinoffExcl = 0
                for date, total in rollingTotal.items():
                    diff = monthDate - datetime.strptime(date, '%Y-%m-%d')
                    if (diff.days < 0):
                        break
                    latestTotal = total
                for date, total in rollingTotalSpinoffExcl.items():
                    diff = monthDate - datetime.strptime(date, '%Y-%m-%d')
                    if (diff.days < 0):
                        break
                    latestTotalSpinoffExcl = total
                monthData['adjustedTotalPrice'] = latestTotal + monthData['price']
                monthData['adjustedTotalPriceSpinoffExcl'] = latestTotalSpinoffExcl + monthData['price']

        with open('./data/extra-data/results/' + fileName, 'w', encoding='utf-8') as f:
            json.dump(transformedData, f, ensure_ascii=False, indent=4)

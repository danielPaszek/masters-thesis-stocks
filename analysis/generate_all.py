import pandas as pd
import numpy as np
import json
import os
import csv
from utils.generateFinalRow import generateFinalRows

from utils.generateRelativeRow import getRelativeRows


ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales',
             'evToGrossProfit', 'priceToGrossProfit']
yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
numericalKeys = ratioKeys + yKeys + y2Keys

# y-no-alpha generated in initial analysis
# resultsPath = '../data/y-no-alpha/'
resultsPath = '../data/extra-data/y-no-alpha/'
pathEqual = '../data/equal-weight-spdr-$.json'
pathSpdr = '../data/spdr-$.json'


def mapDfToCompanyJson(companyDf: pd.DataFrame):
    res = {}
    for index, row in companyDf.iterrows():
        splitedDate = row['date'].split('-')
        year = splitedDate[1]
        month = splitedDate[0]

        if year not in res:
            res[year] = {}
        res[year][month] = row.to_dict()
    return res


def mapCompanyJsonToTemp(companyData):
    res = []
    for year, yearData in companyData.items():
        for month, monthData in yearData.items():
            res.append(monthData)
    return res


def generateFinalRelativeDataFromTemp(tempPath, finalDataPath='../data/final-data-relative/',
                                      tempRelativePath='../data/temp-relative-alpha.csv'):
    allData = []
    relativeDf = pd.read_csv(tempPath, sep='\t')
    offsets = [1, 2]
    dataEqual, dataSpdr = loadSpyData(offsets, pathEqual, pathSpdr)

    dfs = {ticker: data for ticker, data in relativeDf.groupby('ticker')}
    for fileName, data in dfs.items():
        companyData = mapDfToCompanyJson(data)
        generateAlphaForCompanyJson(companyData, dataEqual, dataSpdr, offsets)
        toTempCompany = mapCompanyJsonToTemp(companyData)
        for tempData in toTempCompany:
            allData.append(tempData)
        with open(finalDataPath + fileName.replace('.csv', '.json'), 'w') as f:
            json.dump(companyData, f)
            print('Done' + fileName)

    with open(tempRelativePath, 'w', newline='') as myfile:
        dict_writer = csv.DictWriter(myfile, allData[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(allData)


def generateFinalAbsoluteData(finalDataPath='../data/final-data-absolute/', tempAllPath='../data/temp-all.csv', yPath='../data/extra-data/y-no-alpha/'):
    fileNames = os.listdir(yPath)
    offsets = [1, 2]
    dataEqual, dataSpdr = loadSpyData(offsets, pathEqual, pathSpdr)

    allData = []
    for fileName in fileNames:
        companyDf = pd.read_csv(yPath + fileName, delimiter='\t')
        companyData = mapDfToCompanyJson(companyDf)

        generateAlphaForCompanyJson(companyData, dataEqual, dataSpdr, offsets)

        toTempCompany = mapCompanyJsonToTemp(companyData)
        for tempData in toTempCompany:
            allData.append(tempData)
        with open(finalDataPath + fileName.replace('.csv', '.json'), 'w') as f:
            json.dump(companyData, f)
            print('Done' + fileName)

    with open(tempAllPath, 'w', newline='') as myfile:
        dict_writer = csv.DictWriter(myfile, allData[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(allData)


def generateAlphaForCompanyJson(companyData, dataEqual, dataSpdr, offsets):
    for year, yearData in companyData.items():
        for month, monthData in yearData.items():
            for offset in offsets:
                yearSpy = dataSpdr[offset].get(year, 0)
                monthSpy = yearSpy.get(month, 0) if yearSpy else None
                if not monthSpy:
                    continue
                yearEqual = dataEqual[offset].get(year, 0)
                monthEqual = yearEqual.get(month, 0) if yearEqual else None
                if not monthEqual:
                    continue
                monthData['alpha' + str(offset) + 'Year'] = monthData['yPrice' + str(offset) + 'Year'] - monthSpy[
                    'yPrice']
                monthData['adjustedAlpha' + str(offset) + 'Year'] = monthData['yAdjustedPrice' + str(offset) + 'Year'] - \
                                                                    monthSpy['yAdjustedTotalPrice']

                monthData['equalAlpha' + str(offset) + 'Year'] = monthData['yPrice' + str(offset) + 'Year'] - \
                                                                 monthEqual['yPrice' + str(offset) + 'Year']['mean']
                monthData['equalAdjustedAlpha' + str(offset) + 'Year'] = monthData[
                                                                             'yAdjustedPrice' + str(offset) + 'Year'] - \
                                                                         monthEqual[
                                                                             'yAdjustedPrice' + str(offset) + 'Year'][
                                                                             'mean']


def loadSpyData(offsets, pathEqual, pathSpdr):
    # offset starts at 1
    dataEqual = [0]
    dataSpdr = [0]
    for offset in offsets:
        json_data = open(pathEqual.replace('$', str(offset)))
        dataEqual.append(json.load(json_data))
        json_data = open(pathSpdr.replace('$', str(offset)))
        dataSpdr.append(json.load(json_data))
    return dataEqual, dataSpdr

def generateYnoAlpha(resultsPath='../data/extra-data/results/', yPath='../data/extra-data/y-no-alpha/'):
    # Generate y-no-alpha
    # results(no-alpha) -> y-no-alpha
    fileNames = os.listdir(resultsPath)
    companyDf = pd.DataFrame()
    offsets = [1, 2]
    for fileName in fileNames:
        with open(resultsPath + fileName) as json_data:
            data = json.load(json_data)
            companyDf, i = generateFinalRows(data, ratioKeys, fileName, 0, companyDf, offsets)

            companyDf.to_csv(yPath + fileName.replace('.json', '.csv'), sep='\t')


def generateTempRelative(tempRelPath='../data/extra-data/temp-relative.csv', resultsPath='../data/extra-data/results/'):
    ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales', 'evToGrossProfit', 'priceToGrossProfit']

    if not os.path.isfile(tempRelPath):
        fileNames = os.listdir(resultsPath)
        companyDf = pd.DataFrame()
        i = 0
        for fileName in fileNames:
            with open(resultsPath + fileName) as json_data:
                data = json.load(json_data)
                companyDf, i = getRelativeRows(data, ratioKeys, fileName, i, companyDf, [1,2])
        companyDf.to_csv(tempRelPath, sep='\t')

def combineTemps(absoluteTemp, relativeTemp, combinedInnerPath='../data/extra-data/combined_inner_ticker.csv'):
    absoluteData = pd.read_csv(absoluteTemp)
    absolute = absoluteData.drop('Unnamed: 0', axis=1)
    relativeData = pd.read_csv(relativeTemp)
    relative = relativeData[ratioKeys + ['ticker', 'date']]

    # absoluteData.join(relativeData, on=['date', 'ticker'], how='inner', rsuffix='_relative')
    combinedInnerDf = absolute.merge(relative, on=['ticker', 'date'], how='inner', suffixes=('', '_relative'))
    df = combinedInnerDf.drop(['date'], axis=1)
    df['to_join_id'] = df.index
    # df = combinedInnerDf.drop(['ticker', 'date'], axis=1)
    # df.to_csv('../data/combined_inner.csv')
    df.to_csv(combinedInnerPath)
    return df


if __name__ == "__main__":
    # Before run generate_ratios.py and calculateTotalReturn.py
    tempRelAlpha = '../data/extra-data/temp-relative-alpha.csv'
    tempAll = '../data/extra-data/temp-all.csv'
    # generateYnoAlpha()
    generateTempRelative()
    generateFinalAbsoluteData('../data/extra-data/final-data-absolute/', tempAll)
    generateFinalRelativeDataFromTemp(
        '../data/extra-data/temp-relative.csv',
        '../data/extra-data/final-data-relative/',
        tempRelAlpha
    )
    combineTemps(tempAll, tempRelAlpha)

import pandas as pd
import json
from scipy import stats
from utils.generateFinalRow import getPrices

def getRelativeRows(data, ratioKeys, fileName, i, df):
    for year, yearData in data.items():
        for month, monthData in yearData.items():
            row = generateRow(data, month, monthData, ratioKeys, year, fileName)

            # generateFinalRow::getPrices
            if row is not None:
                nextYears = range(1, 3)  # will be changed to offset range
                for offset in nextYears:
                    nextYear = str(int(year) + offset)
                    nextYearData = data.get(nextYear, 0)
                    if nextYearData:
                        nextMonthData = nextYearData.get(month, 0)
                        if nextMonthData:
                            row = getPrices(monthData, nextMonthData, row, offset)
                toAdd = pd.DataFrame(row, index=[i])
                i += 1
                df = pd.concat([df, toAdd])

    df = df.dropna()
    return df, i

def generateRow(data, month, monthData, ratioKeys, year, fileName):
    row = {}
    fromYear = -3 # change to param or something
    # nextYears = range(1, 3)  # will be changed to offset range
    row['date'] = month + '-' + year
    row['ticker'] = fileName

    relatedRows = getRelatedRows(data, fromYear, month, monthData, year)
    if relatedRows is None:
        return None
    df = pd.DataFrame(relatedRows)
    df.dropna(axis=1, inplace=True)
    # TODO: do magic
    for key in ratioKeys:
        if key in df.columns and monthData.get(key, 0):
            percentile = stats.percentileofscore(df[key], monthData[key])
            row[key] = percentile
    return row

def getRelatedRows(data, fromYear, month, monthData, year):
    month = int(month)
    year = int(year)
    relatedRows = []
    firstYear = data.get(str(year + fromYear), 0)
    if not firstYear:
        return None

    for monthInx in range(month, 13):
        monthData = firstYear.get(str(monthInx), 0)
        if monthData:
            relatedRows.append(monthData)
    for yearOffset in range(fromYear + 1, 0):
        wholeYearToAdd = data.get(str(yearOffset + year), 0)
        if wholeYearToAdd:
            for toAdd in wholeYearToAdd.values():
                relatedRows.append(toAdd)
    lastYear = data.get(str(year), 0)
    if lastYear:
        for monthInx in range(1, month):
            monthData = lastYear.get(str(monthInx), 0)
            if monthData:
                relatedRows.append(monthData)
    return relatedRows


if __name__ == "__main__":
    import pandas as pd
    import json
    import os

    ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales', 'evToGrossProfit', 'priceToGrossProfit']

    if not os.path.isfile('../data/temp-relative.csv'):
        fileNames = os.listdir('../data/results')
        companyDf = pd.DataFrame()
        i = 0
        for fileName in fileNames:
            with open('../data/results/' + fileName) as json_data:
                data = json.load(json_data)
                companyDf, i = getRelativeRows(data, ratioKeys, fileName, i, companyDf)
        companyDf.to_csv('../data/temp-relative.csv', sep='\t')
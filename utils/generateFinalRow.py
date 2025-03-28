import pandas as pd
import json


def generateFinalRows(data, ratioKeys, fileName, i, df):
    for year, yearData in data.items():
        for month, monthData in yearData.items():
            row = generateRow(data, month, monthData, ratioKeys, year, fileName)

            toAdd = pd.DataFrame(row, index=[i])
            i += 1
            df = pd.concat([df, toAdd])

    df = df.dropna()
    return df, i


def generateRow(data, month, monthData, ratioKeys, year, fileName):
    row = {}
    nextYears = range(1, 3)  # will be changed to offset range
    row['date'] = month + '-' + year
    row['ticker'] = fileName

    for offset in nextYears:
        nextYear = str(int(year) + offset)
        nextYearData = data.get(nextYear, 0)
        if nextYearData:
            nextMonthData = nextYearData.get(month, 0)
            if nextMonthData:
                row = mapRow(row, monthData, nextMonthData, ratioKeys)
                row = getPrices(monthData, nextMonthData, row, offset)
    return row


def getPrices(monthData, nextMonthData, row, offset):
    offset = str(offset)
    yPrice = nextMonthData['price'] / monthData['price'] - 1
    yAdjTotalPrice = nextMonthData['adjustedTotalPrice'] / monthData['adjustedTotalPrice'] - 1
    yAdjTotalPriceSpinExcl = nextMonthData['adjustedTotalPriceSpinoffExcl'] / monthData[
        'adjustedTotalPriceSpinoffExcl'] - 1
    row['yAdjustedPriceSpinoffExcl' + offset + 'Year'] = yAdjTotalPriceSpinExcl
    row['yAdjustedPrice' + offset + 'Year'] = yAdjTotalPrice
    row['yPrice' + offset + 'Year'] = yPrice
    return row

def mapRow(row, monthData, nextMonthData, ratioKeys):
    for key in ratioKeys:
        if key in nextMonthData and key in monthData:
            row[key] = monthData[key]
    return row
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
    # ZLE!! - 100div + 100price -> 100div + 50price -> drop 50%, not 25%
    # Poprawione by dzielić przez cenę. diff(price+div) / price
    # Pewnie dało się to zrobić lepiej
    offset = str(offset)
    yPrice = nextMonthData['price'] / monthData['price'] - 1

    deltaAdjTotalPrice = nextMonthData['adjustedTotalPrice'] - monthData['adjustedTotalPrice']
    yAdjTotalPrice = deltaAdjTotalPrice / monthData['price']

    deltaAdjTotalPriceSpinExcl = nextMonthData['adjustedTotalPriceSpinoffExcl'] - monthData['adjustedTotalPriceSpinoffExcl']
    yAdjTotalPriceSpinExcl = deltaAdjTotalPriceSpinExcl / monthData['price']

    row['yAdjustedPriceSpinoffExcl' + offset + 'Year'] = yAdjTotalPriceSpinExcl
    row['yAdjustedPrice' + offset + 'Year'] = yAdjTotalPrice
    row['yPrice' + offset + 'Year'] = yPrice
    return row

def mapRow(row, monthData, nextMonthData, ratioKeys):
    for key in ratioKeys:
        if key in nextMonthData and key in monthData:
            row[key] = monthData[key]
    return row
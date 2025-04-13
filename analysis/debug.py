import pandas as pd
import numpy as np
import json
import os
from utils.generateFinalRow import getPrices
from datetime import datetime


# sp500 prices in spdr-prices.txt -> html table to be parsed
def generateSpyIndex(offset, path):
    spyData = {}
    tables = pd.read_html(path)
    df = tables[0]
#     cleanup dividend notices
    df = df[pd.to_numeric(df['Open'], errors='coerce').notna()]
    df = df[::-1].reset_index(drop=True)

    currMonth = -1
    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%b %d, %Y')
        if date.month == currMonth:
            continue

        currMonth = date.month
        i = index + 1
        for j, nextRow in df.loc[i:].iterrows():
            nextDate = datetime.strptime(nextRow['Date'], '%b %d, %Y')
            if date.year + offset == nextDate.year and date.month == nextDate.month:

# TODO: verify what actually is 'Adj Close' column. Last columns don't have constant close diff. So what exactly it is?
# Total return diff is 2-2,5% when counting dividends. This looks good enough

                if spyData.get(str(date.year),0) == 0:
                    spyData[str(date.year)] = {}

                spyData[str(date.year)][str(date.month)] = {
                    'yPrice': float(nextRow['Close']) / float(row['Close']) - 1,
                    'yAdjustedTotalPrice': float(nextRow['Adj Close']) / float(row['Adj Close']) -1
                }
                break
    print('spy generated')
    return spyData




# THIS IS EQUAL WEIGHT!!!!!!!!
def generateAllEqualWeightIndex(offset, path):
    spyData = {}
    fileNames = os.listdir(path)

    allCompanies = []
    for fileName in fileNames:
        with open(path + fileName) as json_data:
            data = json.load(json_data)
            allCompanies.append(data)

    for year in range(2015, 2026):
        year = str(year)
        for month in range(1, 13):
            month = str(month)
            currentAllData = pd.DataFrame()
            i = 0
            for company in allCompanies:
                yearData = company.get(year, 0)
                monthData = yearData.get(month, 0) if yearData else None
                if not monthData:
                    continue

                nextYearData = company.get(str(int(year) + offset), 0)
                nextMonthData = nextYearData.get(month, 0) if nextYearData else None
                if not nextMonthData:
                    continue

                row = {}
                row = getPrices(monthData, nextMonthData, row, offset)
                currCompany = pd.DataFrame(row, index=[i])
                i += 1
                currentAllData = pd.concat([currentAllData, currCompany])

            if len(currentAllData.index) < 10: # average can't be 1-2 companies
                continue

            stats = {}
            for key in list(currentAllData):
                stats[key] = {
                    'mean': currentAllData.loc[:, key].mean(),
                    'median': currentAllData.loc[:, key].median()
                }
            if spyData.get(year, 0) == 0:
                spyData[year] = {}
            spyData[year][month] = stats

    return spyData


if __name__ == "__main__":
    ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales',
                 'evToGrossProfit', 'priceToGrossProfit']
    yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
    y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
    numericalKeys = ratioKeys + yKeys + y2Keys

    offset = 1 # year return
    for offset in range(1,3):
        path = '../data/spdr-prices.txt'
        spyData = generateSpyIndex(offset, path)
        with open('../data/spdr-' + str(offset) + '.json', 'w') as fp:
            json.dump(spyData, fp)

        path = '../data/results-no-alpha/'
        spyData = generateAllEqualWeightIndex(offset, path)
        with open('../data/equal-weight-spdr-' + str(offset) + '.json', 'w') as fp:
            json.dump(spyData, fp)
    print('Done')
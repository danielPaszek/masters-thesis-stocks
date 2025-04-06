import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
import seaborn as sns
import statistics
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from utils.generateFinalRow import generateFinalRows, getPrices

# from utils.generateRelativeRow import getRelativeRows


ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales',
             'evToGrossProfit', 'priceToGrossProfit']
yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
numericalKeys = ratioKeys + yKeys + y2Keys

path = '../data/results-no-alpha/'
fileNames = os.listdir(path)

allCompanies = []
for fileName in fileNames:
    with open(path + fileName) as json_data:
        data = json.load(json_data)
        allCompanies.append(data)

spyData = {}


# THIS IS EQUAL WEIGHT!!!!!!!!
# sp500 prices in spdr-prices.txt -> html table to be parsed
offset = 1 # year return
for year in range(2015, 2026):
    year = str(year)
    for month in range(1, 13):
        month = str(month)
        currentAllData = pd.DataFrame()
        i = 0
        for company in allCompanies:
            yearData = company.get(year, 0)
            # TODO: REFACTOR!!!!!!!!!!!
            if yearData:
                monthData = yearData.get(month, 0)
                if monthData:
                    nextYearData = company.get(str(int(year) + offset))
                    if nextYearData:
                        nextMonthData = nextYearData.get(month, 0)
                        if nextMonthData:
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
        spyData[month + '-' + year] = stats

with open('../data/all-equal-data.json', 'w') as fp:
    json.dump(spyData, fp)
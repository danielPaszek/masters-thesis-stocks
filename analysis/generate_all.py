import pandas as pd
import numpy as np
import json
import os
import csv
from utils.generateFinalRow import generateFinalRows
# from utils.generateRelativeRow import getRelativeRows


ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales', 'evToGrossProfit', 'priceToGrossProfit']
yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
numericalKeys = ratioKeys + yKeys + y2Keys

resultsPath = '../data/y-no-alpha/'


def mapFinalRowToCompanyJson(companyDf: pd.DataFrame):
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

def generateFinalAbsoluteData():
    pathEqual = '../data/equal-weight-spdr-$.json'
    pathSpdr = '../data/spdr-$.json'

    # load both year files


    fileNames = os.listdir(resultsPath)
    companyDf = pd.DataFrame()
    i = 0
    offsets = [1, 2]
    dataEqual = [0]
    dataSpdr = [0]
    for offset in offsets:
        json_data = open(pathEqual.replace('$', str(offset)))
        dataEqual.append(json.load(json_data))
        json_data = open(pathSpdr.replace('$', str(offset)))
        dataSpdr.append(json.load(json_data))

    allData = []
    for fileName in fileNames:
        # companyDf, i = generateFinalRows(data, ratioKeys, fileName, i, companyDf, offsets) y-no-alpha is this
        companyDf = pd.read_csv(resultsPath + fileName, delimiter='\t')
        companyData = mapFinalRowToCompanyJson(companyDf)

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
                    monthData['alpha'+str(offset)+'Year'] = monthData['yPrice'+str(offset)+'Year'] - monthSpy['yPrice']
                    monthData['adjustedAlpha'+str(offset)+'Year'] = monthData['yAdjustedPrice'+str(offset)+'Year'] - monthSpy['yAdjustedTotalPrice']

                    monthData['equalAlpha'+str(offset)+'Year'] = monthData['yPrice'+str(offset)+'Year'] - monthEqual['yPrice'+str(offset)+'Year']['mean']
                    monthData['equalAdjustedAlpha'+str(offset)+'Year'] = monthData['yAdjustedPrice'+str(offset)+'Year'] - monthEqual['yAdjustedPrice'+str(offset)+'Year']['mean']

        toTempCompany = mapCompanyJsonToTemp(companyData)
        for tempData in toTempCompany:
            allData.append(tempData)
        with open('../data/final-data-absolute/' + fileName.replace('.csv', '.json'), 'w') as f:
            json.dump(companyData, f)
            print('Done' + fileName)

    with open('../data/temp-all.csv', 'w', newline='') as myfile:
        dict_writer = csv.DictWriter(myfile, allData[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(allData)

if __name__ == "__main__":
    generateFinalAbsoluteData()


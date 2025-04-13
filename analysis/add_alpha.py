import pandas as pd
import numpy as np
import json
import os
from utils.generateFinalRow import getPrices
from datetime import datetime
from statistics import geometric_mean

def includeAlphaInResults(pathNoAlpha, pathEqual, pathSpdr):
    fileNames = os.listdir(pathNoAlpha)

    offsets = [1,2]

    # load both year files
    json_data = open(pathEqual)
    dataEqual = json.load(json_data)
    json_data = open(pathSpdr)
    dataSpdr = json.load(json_data)


#                     use yKeys, y2Keys diff with spdr data. Looks ez



if __name__ == "__main__":
    ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales',
                 'evToGrossProfit', 'priceToGrossProfit']
    yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
    y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
    numericalKeys = ratioKeys + yKeys + y2Keys
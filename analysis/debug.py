import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
import seaborn as sns
import statistics
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from utils.generateFinalRow import generateFinalRows

# from utils.generateRelativeRow import getRelativeRows


ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales',
             'evToGrossProfit', 'priceToGrossProfit']
yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
numericalKeys = ratioKeys + yKeys + y2Keys

relativeDf = pd.read_csv('../data/temp-relative.csv', sep='\t')

for key in numericalKeys:
    bin_edges = range(0, 110, 10)
    bin_key = key + '_bin'
    relativeDf[bin_key] = pd.cut(relativeDf[key],bins=bin_edges)
    # sns.boxplot(data=relativeDf, x=key+'_bin', y='yAdjustedPrice1Year')
    sns.barplot(relativeDf, x=bin_key, y='yAdjustedPrice1Year', estimator=np.median)

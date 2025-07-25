from analysis.generate_all import generateFinalAbsoluteData, combineTemps
from cleanupNan import cleanupNan
from headers import *

tempAll = '../data/lstm/data/temp-all.csv'
generateFinalAbsoluteData(tempAllPath=tempAll, yPath='../data/y-no-alpha/', saveEach=False)
cleanupNan(tempAll, tempAll)

tempAllExtra = '../data/lstm/extra-data/temp-all.csv'
generateFinalAbsoluteData(tempAllPath=tempAllExtra, yPath='../data/extra-data/y-no-alpha/', saveEach=False)
cleanupNan(tempAllExtra, tempAllExtra)
from analysis.generate_all import generateFinalAbsoluteData, combineTemps, combineWholeTemps
from cleanupNan import cleanupNan
from headers import *

tempAll = '../data/lstm/data/temp-all.csv'
tempAllExtra = '../data/lstm/extra-data/temp-all.csv'
combinedWholePath = '../data/lstm/combined_whole_ticker.csv'

# generateFinalAbsoluteData(tempAllPath=tempAll, yPath='../data/y-no-alpha/', saveEach=False)
# cleanupNan(tempAll, tempAll)
#
# generateFinalAbsoluteData(tempAllPath=tempAllExtra, yPath='../data/extra-data/y-no-alpha/', saveEach=False)
# cleanupNan(tempAllExtra, tempAllExtra)

combineWholeTemps(tempAll, tempAllExtra, combinedWholePath)
import os

# fileNames = os.listdir('../data/final-data-absolute')
# fileNames2 = os.listdir('../data/final-data-relative')
# diff = list(set(fileNames) - set(fileNames2))
# print(diff)
# print(len(os.listdir('../data/results-no-alpha')))
#
# lost = ['BAC.json', 'TFC.json', 'C.json', 'GEHC.json', 'JPM.json', 'VLTO.json', 'PNC.json', 'SYF.json', 'BX.json', 'CFG.json', 'BK.json', 'CEG.json', 'SCHW.json', 'COF.json', 'SOLV.json', 'APO.json', 'HBAN.json', 'GS.json', 'KKR.json', 'USB.json', 'STT.json', 'AXP.json', 'MTB.json', 'RF.json', 'MS.json', 'FITB.json', 'RJF.json', 'KEY.json', 'KVUE.json', 'DFS.json', 'NTRS.json', 'GEV.json', 'WFC.json']
#
# print(len(os.listdir('../data/extra-data/final-data-absolute')))
fs = os.listdir('../data/extra-data/data')
print(len(fs))
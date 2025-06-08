import pandas as pd

def cleanupNan(
        pathOld='./data/archived/combined_inner_ticker.csv',
        pathNew='./data/extra-data/combined_inner_ticker.csv'
):
    df = pd.read_csv(pathOld)
    df1 = df.dropna()
    df1.to_csv(pathNew, index=False)
import pandas as pd

df = pd.read_csv('./data/archived/combined_inner_ticker.csv')
df1 = df.dropna()
df1.to_csv('./data/extra-data/combined_inner_ticker.csv', index=False)
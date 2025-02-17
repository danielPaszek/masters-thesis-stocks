import pandas as pd

df = pd.read_csv('./data/IVV_holdings.csv')

companies = df[['Ticker', 'Name', 'Exchange']]
companies.to_csv('./data/sp500-left.csv', index=False)
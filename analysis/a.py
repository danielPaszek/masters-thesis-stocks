import pandas as pd

df = pd.read_csv('../data/combined_inner.csv')

print(df.loc[:, 'equalAlpha1Year'].mean())

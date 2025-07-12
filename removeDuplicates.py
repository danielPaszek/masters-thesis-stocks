from utils.custom_train_test_split import joinDfs
import pandas as pd

files = ['./data/combined_inner_ticker.csv', './data/extra-data/combined_inner_ticker.csv']

df = joinDfs(files)
df['date'] = pd.to_datetime(df['date'], format='%m-%Y')
deduplicated = df.groupby(['ticker', 'date'], as_index=False).first()
# unnamed issue
df = deduplicated.loc[:, ~deduplicated.columns.str.match('Unnamed')]
df.to_csv('./data/deduplicated/combined_inner_ticker.csv', index=False)
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import random

exchange = {
    'NASDAQ': 'NasdaqGS',
    'New York Stock Exchange Inc.': 'NYSE'
}
driver = webdriver.Chrome()
search_url = 'https://workers.finchat.io/company/$$$-&&&/valuation'

df = pd.read_csv('./data/sp500-left.csv')

for index, row in df.iterrows():
    url = search_url.replace('$$$', exchange[row['Exchange']]).replace('&&&', row['Ticker'])
    print(url)
    driver.get(url)
    sleep(random.randint(2,7))
    body = driver.find_element(By.XPATH, '//body/pre').get_attribute('innerHTML')
    f = open('./data/' + row['Ticker'] + '.json', 'w')
    f.write(body)
    print(index)

# missing XTSLA,BLK CSH FND TREASURY SL AGENCY,-
# CBOE,CBOE GLOBAL MARKETS INC,Cboe BZX formerly known as BATS
#
import pandas as pd
import json
from utils.mappingUtils import *
from datetime import datetime
import os

fileNames = os.listdir('./data/data')

for fileName in fileNames:
    with open('./data/data/' + fileName) as json_data:
        try:
            data = json.load(json_data)
        except:
            print('Error reading ' + fileName)
            with open('./data/error/' + fileName, 'w', encoding='utf-8') as f:
                f.write(json_data.read())

        mapped = {}
        for obj in data['data']:
            mapped[obj['date']] = mapRawToObj(obj)

        years = getYearsMap(mapped)

        results = {}
        # calc closest to dates
        for year in years.keys():
            for month in range(1,13):
                minDays = 15
                minReading = None
                for reading in years[year]:
                    date = datetime.strptime(reading['date'], '%Y-%m-%d')
                    if month == date.month:
                        if date.day < minDays:
                            minDays = date.day
                            minReading = reading
                if minReading:
                    if year not in results:
                        results[year] = {}
                    results[year][month] = minReading
        with open('./data/transformed/' + fileName, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(fileName + ' saved')


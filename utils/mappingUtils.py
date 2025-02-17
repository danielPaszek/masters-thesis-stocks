from datetime import datetime

def mapRawToObj(obj):
    res = {}
    for key in obj.keys():
        if key in [
            'exchangeRate', 'priceToFFO', 'forwardPriceToFFO', 'priceToAdjustedFFO', 'forwardPriceToAdjustedFFO',
            '4038', '100054', '100060'
                   ]:
            continue
        val = obj[key]
        if type(val) is str and val.isnumeric():
            val = float(val)
        if type(val) is int or type(val) is float:
            val = round(val, 2)
        if key == '100052':
            key = 'price'
        res[key] = val
    return res


def getYearsMap(mapped):
    years = {}
    for readingDate in mapped.keys():
        date = datetime.strptime(readingDate, '%Y-%m-%d')
        if date.year not in years.keys():
            years[date.year] = []
        years[date.year].append(mapped[readingDate])
    return years

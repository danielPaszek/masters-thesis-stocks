Python 3.12

trained svm models:
analysis/models/*.joblib
training - analysis/svm_predict.py



./data:
- data - responses from API
- error - failed responses
- error-data - data we got for failed tickers
- final-data-absolute - includes alpha, yPrices and absolute values of ratios
- final-data-relative - includes alpha, yPrices and relative values of ratios
- market-data - dividends from API
- random - ...
- results-no-alpha - combine prices and dividends sources
- temp
- transformed - mapped from responses to parceable form
- y-no-alpha - calculated yPrices
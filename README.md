Python 3.12

TODO: year split implementation. Model can see apple previous data, but not latest

trained svm models:
analysis/models/*.joblib
training - analysis/svm_predict.py

They weren't trained on company custom split!!!
analysis/models2/*.joblib - models trained on cutoff = 0.0
Too much computation required to train all labels with all cutoffs
- Even without adjusting cutoff there are very good results, but linear also did well on random split
- NEVER TRAINED ON CUSTOM SPLIT - TODO: THIS
- results between 5-15% cagr better than alpha

[general_learning.ipynb](analysis%2Fgeneral_learning.ipynb):
- adjusted cutoff, tried using balanced classes
- USED company split
- drew results and comparisons - basically ready for paper

[svr_learning.ipynb](analysis%2Fsvr_learning.ipynb)
- TRAGIC RESULTS - R2 = 0 - model as good as average y
- USED company split
- no surprise - SLR told this was difficult, not really scope of this paper, but still
- 


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
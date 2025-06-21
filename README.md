Python 3.12

TODO: create new dataset for LSTM, because we no longer need _relative

TODO: w regresji puścić na combined datasecie, obecnie jest tylko data/combiner_inner

TODO: banalny test t studenta na każdym parametrze np cutoff = mean(PE), sprawdzający czy to działa. Potem jak mam histogramy to również test t studenta na każdym binie

TODO: year split implementation. Model can see apple previous data, but not latest - DONE, but not used everywhere

trained svm models:
analysis/models/*.joblib
training - analysis/svm_predict.py

They weren't trained on company custom split!!!
analysis/models2/*.joblib - models trained on cutoff = 0.0
Too much computation required to train all labels with all cutoffs
- Even without adjusting cutoff there are very good results, but linear also did well on random split
- NEVER TRAINED ON CUSTOM SPLIT - TODO: THIS
- results between 5-15% cagr better than alpha

TODO: predict_proba for LinearSVC in general_learning and year_learning -> ONE FINAL NOTEBOOK?
[general_learning.ipynb](analysis%2Fgeneral_learning.ipynb):
- adjusted cutoff, tried using balanced classes
- USED company split
- drew results and comparisons - basically ready for paper

[year_learning.ipynb](analysis%2Fyear_learning.ipynb):
- this is copy of general_learning but run on split year dataset

[svr_learning.ipynb](analysis%2Fsvr_learning.ipynb)
- TRAGIC RESULTS - R2 = 0 - model as good as average y
- USED company split
- no surprise - SLR told this was difficult, not really scope of this paper, but still
- 

[linear_svm.ipynb](analysis%2Flinear_svm.ipynb):
- general_learning is better file. This was first try
- cv on cutoff=0, results acceptable
- BUT regular train_test_split!

[linear_analysis.ipynb](analysis%2Flinear_analysis.ipynb)

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
- combined_inner_ticker - 
  - updated 08.06.2025 - added date because we need date split too. There shouldn't be data leaks in any model
  - before - added ./data/extra-data with 501-700 companies marketcap in USA

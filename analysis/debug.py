from analysis.training_helper import trainPipeline
from utils.custom_train_test_split import per_year_train_test_split
import matplotlib.pyplot as plt

files = ['../data/deduplicated/combined_inner_ticker.csv']
cutoffs = [0.0, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20, 0.25, 0.35]
thresholds = [70, 80, 90, 95]


trainDf, testDf = per_year_train_test_split(files, format='%Y-%m-%d')
resultsToPlotYear = trainPipeline(cutoffs, ['alpha1Year'], trainDf, testDf, thresholds)


plt.plot(cutoffs, resultsToPlotYear['alpha1Year'], marker='o', linestyle='-', color='b', label='Data')

plt.xlabel('cutoff')
plt.ylabel('% of ones')
plt.title('Cutoff influence on % of ones in dataset')
plt.grid(True)
plt.legend()

plt.show()
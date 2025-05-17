ratioKeys = ['psRatio', 'peRatio', 'priceToBook', 'evToEbitda', 'evToEbit', 'priceToFreeCashFlow', 'evToSales', 'evToGrossProfit', 'priceToGrossProfit']
yKeys = ['yAdjustedPriceSpinoffExcl1Year', 'yAdjustedPrice1Year', 'yPrice1Year']
y2Keys = ['yAdjustedPriceSpinoffExcl2Year', 'yAdjustedPrice2Year', 'yPrice2Year']
yAlpha = ['alpha1Year','adjustedAlpha1Year','equalAlpha1Year','equalAdjustedAlpha1Year','alpha2Year','adjustedAlpha2Year','equalAlpha2Year','equalAdjustedAlpha2Year']

numericalKeys = ratioKeys + yKeys + y2Keys
relativeRatioKeys = [x + '_relative' for x in ratioKeys]
from statsmodels.tsa.stattools import coint

def run_cointegration_test(series1, series2):
    return coint(series1, series2)[1] 

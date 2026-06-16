from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from itertools import combinations


def adf_test(series):
    result = adfuller(series)
    p_value = result[1]
    return p_value

def cointegration_test(series_a, series_b):
    constant = sm.add_constant(series_b)
    model = sm.OLS(series_a, constant).fit()
    residuals = model.resid
    result = adf_test(residuals)
    return result

def find_cointegrated_pairs(prices, pvalue_threshold=0.05):
    pairs = list(combinations(prices.columns, 2))
    result = []
    for i in pairs:
        p_value = cointegration_test(prices[i[0]], prices[i[1]])
        if p_value <= pvalue_threshold:
            result.append((i[0],i[1], round(p_value, 4)))
    return result


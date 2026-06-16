import numpy as np
import statsmodels.api as sm
import pandas as pd
from src.cointegration import find_cointegrated_pairs

def calculate_spread(series_a, series_b):
    constant = sm.add_constant(series_b)
    model = sm.OLS(series_a, constant).fit()
    hedge_ratio = model.params.iloc[1]
    spread = series_a - hedge_ratio * series_b
    return spread

def calculate_half_life(spread):
    spread_lag = spread.shift(1)  #spread(t-1)
    delta_spread = spread.diff()  #spread(t) - spread(t-1)
    data = pd.concat([delta_spread, spread_lag], axis=1).dropna()
    constant = sm.add_constant(data.iloc[:, 1])
    model = sm.OLS(data.iloc[:, 0], constant).fit()
    return -np.log(2) / np.log(1 + model.params.iloc[1])

def select_pairs(prices, cointegrated_pairs, top_n=5, min_half_life=5, max_half_life=126):
    temp = []
    for i in cointegrated_pairs:
        spread = calculate_spread(prices[i[0]], prices[i[1]])
        half_life = calculate_half_life(spread)
        if half_life < min_half_life or half_life > max_half_life:
            continue
        else:
            temp.append({
                "ticker_a": i[0],
                "ticker_b": i[1],
                "p_value": i[2],
                "half_life": round(half_life, 1)
            })
    
    temp.sort(key=lambda x:x["p_value"])
    return temp[:top_n]


import numpy as np
import pandas as pd

def sharpe_ratio(returns):
    sharpe = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
    return sharpe

def max_drawdown(cumulative_pnl):
    rolling_max = cumulative_pnl.cummax()
    drawdown = cumulative_pnl - rolling_max
    max_drawdown = drawdown.min()
    return max_drawdown

def calmar_ratio(returns, cumulative_pnl):
    annualized_return = np.mean(returns) * 252
    dd = abs(max_drawdown(cumulative_pnl))
    if dd == 0:
        return np.nan
    calmar = annualized_return / abs(max_drawdown(cumulative_pnl))
    return calmar
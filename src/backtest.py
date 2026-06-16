import numpy as np
import pandas as pd

def run_backtest(spread, signals, transaction_cost=0.001):
    spread_change = spread.diff()
    prev_signal = signals.shift(1)
    daily_return = prev_signal * spread_change
    trade_occured = signals != prev_signal
    costs = trade_occured * transaction_cost
    net_return = daily_return - costs
    cumulative_return = net_return.cumsum()
    return cumulative_return
        
import numpy as np
import pandas as pd

def generate_signals(spread, half_life):
    window = max(2, int(half_life))
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    z_score = (spread - rolling_mean) / rolling_std
    signals = pd.Series(np.nan, index=spread.index, dtype=float)
    signals[z_score < -2] = 1.0  #Buy spread
    signals[z_score > 2] = -1.0  #Short spread
    signals[z_score.abs() < 0.5] = 0.0 #Exit position

    if pd.isna(signals.iloc[0]):
        signals.iloc[0] = 0.0
    
    signals = signals.ffill()

    return z_score, signals
    
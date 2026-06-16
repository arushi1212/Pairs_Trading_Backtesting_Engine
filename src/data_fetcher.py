import yfinance as yf
from src.universe import FINANCIAL_UNIVERSE, START_DATE, END_DATE
import pandas as pd
import os

def load_data(filename, tickers, start, end):
    if os.path.exists(filename):
        print(f"File '{filename}' already exists")
        return pd.read_csv(filename, index_col=0, parse_dates=True)
    
    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        group_by='ticker'
    )

    prices = data.xs("Close", axis=1, level=1)
    prices.to_csv(filename, index=True)

    return pd.read_csv(filename, index_col=0, parse_dates=True)









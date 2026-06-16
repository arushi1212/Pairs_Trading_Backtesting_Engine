import os
import yfinance as yf
import pandas as pd
from src.data_fetcher import load_data
from src.universe import FINANCIAL_UNIVERSE, START_DATE, END_DATE
from src.cointegration import find_cointegrated_pairs
from src.pair_selector import select_pairs


filename = "stock_prices.csv"
stock_df = load_data(filename, FINANCIAL_UNIVERSE, START_DATE, END_DATE)

pairs = find_cointegrated_pairs(stock_df)

selected = select_pairs(stock_df, pairs)
for i in selected:
    print(i)

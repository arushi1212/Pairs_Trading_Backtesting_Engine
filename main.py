import os
import yfinance as yf
import pandas as pd
from src.data_fetcher import load_data
from src.universe import FINANCIAL_UNIVERSE, START_DATE, END_DATE
from src.cointegration import find_cointegrated_pairs
from src.pair_selector import select_pairs, calculate_spread
from src.signals import generate_signals
from src.backtest import run_backtest


filename = "stock_prices.csv"
stock_df = load_data(filename, FINANCIAL_UNIVERSE, START_DATE, END_DATE)

pairs = find_cointegrated_pairs(stock_df)

selected = select_pairs(stock_df, pairs)

top_pair = selected[0]
spread = calculate_spread(stock_df[top_pair["ticker_a"]], stock_df[top_pair["ticker_b"]])
z_score, signals = generate_signals(spread, top_pair["half_life"])

print(signals.value_counts())

cumulative_pnl = run_backtest(spread, signals)
print(cumulative_pnl.tail())
print(f"Total PnL: {cumulative_pnl.iloc[-1]:.2f}")

import streamlit as st
import datetime
from src.data_fetcher import load_data
from src.cointegration import find_cointegrated_pairs
from src.pair_selector import select_pairs
from src.universe import FINANCIAL_UNIVERSE, START_DATE, END_DATE
from src.pair_selector import calculate_spread
from src.signals import generate_signals
from src.backtest import run_backtest
from src.metrics import sharpe_ratio, max_drawdown, calmar_ratio
from src.visualizer import plot_results

@st.cache_data
def load_pipeline():
    prices = load_data("stock_prices.csv", FINANCIAL_UNIVERSE, START_DATE, END_DATE)
    pairs = find_cointegrated_pairs(prices)
    selected = select_pairs(prices, pairs)
    return prices, selected

prices, selected = load_pipeline()


st.title("Pairs Trading Backtesting Engine")

#Sidebar for selecting the pairs, dates
st.sidebar.header("Parameters")

selected_pair_dict = st.sidebar.selectbox(
    label="Select Cointegrated Stock Pair",
    options=selected,
    format_func=lambda pair: f"{pair['ticker_a']} / {pair['ticker_b']} (p={pair['p_value']:.4f})"
)

ticker_a = selected_pair_dict["ticker_a"]
ticker_b = selected_pair_dict["ticker_b"]
half_life = selected_pair_dict["half_life"]

st.sidebar.subheader("Backtest Parameters")
default_start = datetime.date(2020,1,1)
default_end = datetime.date(2024,12,31)

date_range = st.sidebar.date_input(
    label="Select Backtest Date Range",
    value=(default_start, default_end),
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date(2024, 12, 31)
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = default_start, default_end


tc_value = st.sidebar.slider(
    label="Transaction Cost (per share/unit)",
    min_value=0.0000,
    max_value=0.0100,
    value=0.0010,
    step=0.0005,
    format="%.4f"
)

ticker_a = selected_pair_dict["ticker_a"]
ticker_b = selected_pair_dict["ticker_b"]
half_life = selected_pair_dict["half_life"]

filtered_prices = prices.loc[str(start_date): str(end_date)]

spread = calculate_spread(filtered_prices[ticker_a], filtered_prices[ticker_b])
z_score, signals = generate_signals(spread, half_life)

cumulative_pnl = run_backtest(spread, signals, transaction_cost=tc_value)

returns = cumulative_pnl.diff().dropna()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total PnL", f"{cumulative_pnl.iloc[-1]:.2f}")
col2.metric("Sharpe Ratio", f"{sharpe_ratio(returns):.2f}")
col3.metric("Max Drawdown", f"{max_drawdown(cumulative_pnl):.2f}")
col4.metric("Calmar Ratio", f"{calmar_ratio(returns, cumulative_pnl):.2f}")

st.title("Plots")
plots = plot_results(spread, z_score, signals, cumulative_pnl, f"{ticker_a}/{ticker_b}")

st.pyplot(plots)


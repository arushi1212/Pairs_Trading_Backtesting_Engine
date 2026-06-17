# **Pairs Trading Backtesting Engine**

## **Overview**
This project implements a systematic pairs trading and backtesting platform. It identifies statistically tradable pairs from a universe of large-cap financial sector stocks using cointegration testing, then evaluates a mean-reversion strategy on those pairs through a realistic backtesting pipeline.

The goal is to explore the effectiveness of mean-reversion-based pairs trading while emphasizing realistic backtesting practices: lookahead bias prevention, transaction cost modeling, and systematic pair selection.

Intuition: certain securities exhibit stable long-term relationships due to similar business models, industry exposure, or shared economic drivers (e.g.Fed policy, credit cycles). When the relative pricing between two such securities diverges significantly from its historical relationship, that spread tends to revert back toward equilibrium over time.

## **Strategy Logic**
The pipeline runs in five stages:

1. Data acquisition: download adjusted close prices for 10 large-cap financial tickers (2020-2024) via yfinance, cached locally as CSV.

2. Pair discovery: test all 45 possible pairs for cointegration using Engle-Granger method: regress stock A on stock B, then run an Augmented Dickey-Fuller (ADF) test on the regression residuals. A pair is considered conintegrated if the residuals are stationary (p < 0.05).

3. Pair selection: rank cointegrated pairs by p-value and filter by half-life of mean reversion (kept between 5 and 126 trading days, i.e., tradeable but not noise). THe top 5 pairs are selected for backtesting.

4. Signal generation: compute the spread using the OLS hedge ratio, then a rolling z-score of that spread. Enter long/short at |z| > 2, exit at |z| < 0.5.

5. Backtest and evaluation: simulate PnL using lagged signals and transaction costs, then evaluate using Sharpe ratio, max drawdown, and Calmar ratio.

## **Installation & Usage**
git clone https://github.com/arushi1212/Pairs_Trading_Backtesting_Engine.git

cd Pairs_Trading_Backtesting_Engine

pip install -r requirements.txt

#Run the full pipeline

python main.py

#Launch the interactive dashboard

streamlit run app.py

The dashboard lets you select a pair, adjust the backtest date range, and tune transaction costs in real time, with metrics and plots updating live.

## **Results**
Out of 45 possible pairs across the financial universe, 13 were found to be cointegrated (p < 0.05). The top 5 by statistical strength:

| **Pair** | **p-value** | **Half-life(days)**|
| -------- | -------- | -------- |
|GS/WFC| 0.0003 | 42.5|
|AXP/WFC| 0.0007 | 34.2 |
|WFC/MS| 0.0018 | 50.0 |
|BLK/COF| 0.0047 | 37.3 |
|BLK/C | 0.0048 | 65.0|

The strongest pair by statistical significance was GS/WFC, with cointegration p-value of 0.0003 and an estimated mean-reversion half-life of 42.5 trading days.

**GS/WFC Backtest Performace**
| **Metric** | **Value** |
| -------- | -------- |
|Total PnL| -26.58|
|Sharpe Ratio| -0.11|
|Max Drawdown| -87.86|
|Calmar Ration| -0.06|

The figure below illustrates cumulative PnL, drawdown, and z-score based trading signals for the GS/WFC pair.


## **Lookahead Bias & Walk*Forward Validation**
Lookahead bias occurs when a backtest uses information that would not actually have been available at the time a trading decision was made. It produces unrealistically optimistic performance, since the strategy is effectively trading with knowledge of the future.

**Where is could occur in this project, and how it was handled:**
1. Signal-to-trade timing: Trading signals are generated using yesterday's signal applied to today's price change (signal.shift(1)), not today's signal applied to today's return. In live trading, a signal observed at today's close can only be acted on starting the next trading session — using same-day signal and return would assume an impossible instantaneous execution.

2. Z-score normalization: The rolling mean and standard deviation used to compute the z-score are calculated using only a trailing window (sized to the pair's half-life), not the full 5-year sample. Using the full-sample mean/std would mean a trade made in 2020 is implicitly informed by price data from 2024 — information that didn't exist yet.

3. Pair selection (current limitation): Cointegration testing and pair ranking in this version are run on the full 2020–2024 sample before backtesting. This means the strategy "knows" in advance which pairs will be cointegrated over the full window, which is itself a form of lookahead bias and likely explains why some pairs underperform once transaction costs are applied. This is the primary limitation of the current version and is addressed by the walk-forward approach.

**Next step - Walk-Forward validation:** The historical data would be split into rolling training and testing windows (e.g. a 2-year training period followed by a 6-month out-of-sample test period, then rolled forward). Cointegration testing, hedge ratio estimation, and half-life calculation would be performed only on each training window, with signals generated and PnL measured only on the corresponding unseen test window. Repeating this across multiple windows would test whether a pair's cointegration relationship is genuinely stable enough to trade, rather than a full-sample artifact, and would give a more honest estimate of live performance.

## **Tech Stack**
Python, pandas, NumPy, statsmodels (ADF test, OLS regression), yfinance, Streamlit, Matplotlib
**



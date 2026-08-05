import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

STARTING_CASH = 10_000
TICKER = "AAPL"

# Download historical prices
data = yf.download(
    TICKER,
    start="2010-01-01",
    end="2025-01-01",
    auto_adjust=True,
)

close = data["Close"].squeeze()

# Calculate daily returns
daily_returns = close.pct_change().fillna(0)

cum_returns = (1 + daily_returns).cumprod()
# Buy-and-hold benchmark
buy_and_hold = STARTING_CASH * cum_returns

# Moving-average strategy
fast_average = close.rolling(50).mean()
slow_average = close.rolling(200).mean()

signal = (fast_average > slow_average).astype(float)

# Wait until the following trading day before acting on a signal
position = signal.shift(1).fillna(0)
COST_RATE = 0.0005

# Measures how much of the portfolio is bought or sold
turnover = position.diff().abs().fillna(position.abs())

# Apply the trading cost whenever the position changes
trading_cost = turnover * COST_RATE

strategy_returns = (
    position * daily_returns
    - trading_cost
)



cumMovingAvgReturns = (1 + strategy_returns).cumprod()
strategy_value = STARTING_CASH * cumMovingAvgReturns

# Calculate the length of the backtest in years
number_of_days = (close.index[-1] - close.index[0]).days
number_of_years = number_of_days / 365.25

# Calculate annualized returns
buy_and_hold_annual_return = (
    cum_returns.iloc[-1] ** (1 / number_of_years)
) - 1

moving_average_annual_return = (
    cumMovingAvgReturns.iloc[-1] ** (1 / number_of_years)
) - 1

# Display results
print(f"Buy and hold: ${buy_and_hold.iloc[-1]:,.2f}")
print(f"Moving-average strategy: ${strategy_value.iloc[-1]:,.2f}")
print(f"With buy-and-hold strategy, money increased by {cum_returns.iloc[-1]:,.2f}x, and growth was {buy_and_hold_annual_return:.2%} per year")
print(f"With moving-average strategy, money increased by {cumMovingAvgReturns.iloc[-1]:,.2f}x, and growth was {moving_average_annual_return:.2%} per year")
# anual growth per year = total growth %/years
 
pd.DataFrame(
    {
        "Buy and hold": buy_and_hold,
        "Moving-average strategy": strategy_value,
    }
).plot(title=f"{TICKER} Strategy Comparison")

plt.ylabel("Portfolio value ($)")
plt.show()
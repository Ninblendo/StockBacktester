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

# Buy-and-hold benchmark
buy_and_hold = STARTING_CASH * (1 + daily_returns).cumprod()

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

strategy_value = STARTING_CASH * (
    1 + strategy_returns
).cumprod()


strategy_value = STARTING_CASH * (1 + strategy_returns).cumprod()

# Display results
print(f"Buy and hold: ${buy_and_hold.iloc[-1]:,.2f}")
print(f"Moving-average strategy: ${strategy_value.iloc[-1]:,.2f}")

pd.DataFrame(
    {
        "Buy and hold": buy_and_hold,
        "Moving-average strategy": strategy_value,
    }
).plot(title=f"{TICKER} Strategy Comparison")

plt.ylabel("Portfolio value ($)")
plt.show()
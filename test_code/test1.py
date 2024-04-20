import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

# Define symbol and timeframe
symbol = "TCS.NS"

# Download historical data (replace with your data source)
data = pd.read_csv("dataset/symbol_data.csv", index_col="Date", parse_dates=True)  # Change filename and format

# Calculate Supertrend with same parameters as TradingView
supertrend = ta.supertrend(high=data["High"], low=data["Low"], close=data["Close"], period=10, multiplier=3)

# Plot Supertrend and price (similar visualization)
fig, ax1 = plt.subplots()

ax1.plot(supertrend.index, data["Close"], label="Close Price")
ax1.plot(supertrend.index, supertrend["SUPERT_10_3.0"], label="Supertrend", color='blue')

ax1.set_ylabel("Price", color='black')
plt.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.fill_between(
    supertrend.index, supertrend["SUPERTl_10_3.0"], supertrend["SUPERTs_10_3.0"], where=(supertrend["SUPERTd_10_3.0"] == 1), color='green', alpha=0.3, label="Up Trend Channel"
)
ax2.fill_between(
    supertrend.index, supertrend["SUPERTl_10_3.0"], supertrend["SUPERTs_10_3.0"], where=(supertrend["SUPERTd_10_3.0"] == -1), color='red', alpha=0.3, label="Down Trend Channel"
)
ax2.set_ylabel("Supertrend", color='blue')
plt.legend(loc="upper right")

plt.title(f"Supertrend ({symbol})")
plt.show()

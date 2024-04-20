import pandas as pd
import matplotlib.pyplot as plt
from yfinance import Ticker
import numpy as np

def fetch_live_data(symbol):
    latest_data = Ticker(symbol).history(interval="1m", period="1d")
    return latest_data

def pine_supertrend(factor, atr_period, close):
    src = (close[:, 0] + close[:, 1]) / 2
    atr = np.zeros_like(src)
    atr[0] = src[1] - src[0]
    for i in range(1, len(src)):
        atr[i] = max(abs(src[i] - src[i-1]), abs(src[i] - close[i-1][1]), abs(close[i-1][1] - src[i-1]))

    upper_band = src + factor * atr
    lower_band = src - factor * atr

    prev_lower_band = lower_band[0]
    prev_upper_band = upper_band[0]

    super_trend = np.zeros_like(src)
    direction = np.zeros_like(src)

    for i in range(len(src)):
        if i == 0:
            direction[i] = 1
        elif prev_upper_band == prev_upper_band:
            direction[i] = -1 if close[i][1] > upper_band[i] else 1
        else:
            direction[i] = 1 if close[i][1] < lower_band[i] else -1

        super_trend[i] = lower_band[i] if direction[i] == -1 else upper_band[i]

        prev_lower_band = lower_band[i] if lower_band[i] > prev_lower_band or close[i][1] < prev_lower_band else prev_lower_band
        prev_upper_band = upper_band[i] if upper_band[i] < prev_upper_band or close[i][1] > prev_upper_band else prev_upper_band

    return super_trend, direction

def main(symbol, factor, atr_period):
    symbol_data = fetch_live_data(symbol)
    close_prices = symbol_data[['Open', 'Close']].values
    super_trend_py, direction_py = pine_supertrend(factor, atr_period, close_prices)

    Pine_Supertrend = [0]  # Dummy initialization for Pine Script function
    pineDirection = [0]  # Dummy initialization for Pine Script function
    # Update Pine_Supertrend and pineDirection with values obtained from Pine Script function

    # Compare outputs
    plt.plot(super_trend_py, label="Python Supertrend", color='blue')
    plt.plot(Pine_Supertrend, label="Pine Script Supertrend", color='orange')
    plt.legend()
    plt.show()

    print("Python Supertrend:", super_trend_py[-1])
    print("Pine Script Supertrend:", Pine_Supertrend[-1])

    print("Python Direction:", direction_py[-1])
    print("Pine Script Direction:", pineDirection[-1])

symbol = "TCS.NS"
factor = 2
atr_period = 20
main(symbol, factor, atr_period)

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

def plot_supertrend_with_symbol_data(super_trend, direction, symbol_data):
    fig, ax1 = plt.subplots()

    # Determine the color based on the direction
    line_color = 'green' if direction[-1] == 1 else 'red'

    ax1.plot(symbol_data.index, super_trend, label="Supertrend", color=line_color)

    ax1.set_ylabel('Supertrend')
    ax1.tick_params('y')

    ax2 = ax1.twinx()
    ax2.plot(symbol_data.index, symbol_data["Close"], label="Close", color='blue')
    ax2.set_ylabel('TCS Current Price')
    ax2.tick_params('y', colors='blue')

    fig.tight_layout()
    plt.legend()
    plt.show()
    plt.pause(60)
    plt.close()



def main(symbol, factor, atr_period):
    while True:
        symbol_data = fetch_live_data(symbol)
        close_prices = symbol_data[['Open', 'Close']].values
        super_trend, direction = pine_supertrend(factor, atr_period, close_prices)
        plot_supertrend_with_symbol_data(super_trend, direction, symbol_data)
        # Calculate 1% of stock price
        one_percent_price = symbol_data["Close"] * 0.01
        # Check if the difference between supertrend and close price is less than 1% of stock price
        if abs(super_trend[-1] - symbol_data["Close"].iloc[-1]) < one_percent_price.iloc[-1]:
            print("Supertrend:", super_trend[-1])
            print("Close Price:", symbol_data["Close"].iloc[-1])
            print("1% of Stock Price:", one_percent_price.iloc[-1])
            break  # Exit loop if condition met

symbol = "TCS.NS"
factor = 2
atr_period = 20
main(symbol, factor, atr_period)

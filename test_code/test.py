import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt 
from yfinance import Ticker
import numpy as np

symbol = "TCS.NS"

atr_length = 20
factor = 2

has_fetched_full_day_data = False

def fetch_live_data(symbol):
    global has_fetched_full_day_data, symbol_data
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

# Assuming close_prices is a 2D array where each row contains [open, close] prices
close_prices = np.array([[open_price, close_price] for open_price, close_price in zip(open_prices, close_prices)])
factor = 3
atr_period = 10

Pine_Supertrend, pineDirection = pine_supertrend(factor, atr_period, close_prices)

# You can now use Pine_Supertrend and pineDirection arrays for further analysis or plotting.

def plot_supertrend_with_symbol_data(super_trend, symbol_data):
    fig, ax1 = plt.subplots()

    for index, row in super_trend.iterrows():
        print(index, row['SUPERTd_7_3.0'])

    ax1.plot(super_trend.index, super_trend['SUPERTl_7_3.0'], label="Supertrend", color='red')
    ax1.plot(super_trend.index, super_trend['SUPERTs_7_3.0'], label="Supertrend", color='green')

    ax1.set_ylabel('Supertrend', color='blue')
    ax1.tick_params('y', colors='blue')

    # Creating a second y-axis for symbol data
    ax2 = ax1.twinx()
    ax2.plot(symbol_data.index, symbol_data["Close"], label="Close", color='blue')  # Example: Close price
    ax2.set_ylabel('TCS Current Prize', color='red')
    ax2.tick_params('y', colors='red')

    fig.tight_layout()
    plt.ion()
    plt.legend()
    plt.show()
    plt.pause(60)
    plt.close()

def plot_supertrend_with_symbol_data(super_trend, symbol_data):
    fig, ax1 = plt.subplots()

    ax1.plot(super_trend.index, super_trend['SUPERTl_7_3.0'], label="Supertrend Long", color='red')
    ax1.plot(super_trend.index, super_trend['SUPERTs_7_3.0'], label="Supertrend Short", color='green')

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

def main(symbol):
    global atr_length, factor
    data = fetch_live_data(symbol)
    super_trend = calculate_supertrend(data)
    print('super_trend:', atr_length, factor, super_trend)
    # plot_supertrend_with_symbol_data(super_trend, data)

main(symbol)

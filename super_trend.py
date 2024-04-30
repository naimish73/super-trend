import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt  
from yfinance import Ticker
import numpy as np

symbol = "TCS.NS"

has_fetched_full_day_data = False
symbol_data = pd.DataFrame()

def fetch_live_data(symbol):
    global has_fetched_full_day_data, symbol_data
    if has_fetched_full_day_data:

        latest_data = Ticker(symbol).history(interval="1m", period='1m')
        latest_data = latest_data.iloc[-1:]

        symbol_data = pd.concat([symbol_data, latest_data])
    else:

        symbol_data = Ticker(symbol).history(interval="1m", period='1d')
        has_fetched_full_day_data = True

    return symbol_data


def calculate_supertrend(data):
    atrPeriod = 20  
    factor = 2.0    

    supertrend = data.ta.supertrend(length=20, multiplier=2.0)
    data.reset_index(inplace=True)
    supertrend.reset_index(inplace=True)

    merged_df = pd.merge(data, supertrend, on="Datetime")
    merged_df.to_csv('dataset/super_trend.csv')

    return merged_df


def plot_supertrend_with_symbol_data(super_trend, symbol_data):
    fig, ax1 = plt.subplots()

    ax1.plot(super_trend.index, super_trend['SUPERTl_20_2.0'], label="Supertrend", color='green')
    ax1.plot(super_trend.index, super_trend['SUPERTs_20_2.0'], label="Supertrend", color='red')

    ax1.set_ylabel('Supertrend', color='red')
    ax1.tick_params('y', colors='red')

    ax2 = ax1.twinx()
    ax2.plot(symbol_data.index, symbol_data["Close"], label="Close", color='blue')  
    ax2.set_ylabel('TCS Current Prize', color='blue')
    ax2.tick_params('y', colors='blue')

    fig.tight_layout()
    plt.ion()
    plt.legend()
    plt.show(block=True)


def main(symbol):

    data = fetch_live_data(symbol)
    super_trend = calculate_supertrend(data)
    plot_supertrend_with_symbol_data(super_trend, data)

main(symbol)
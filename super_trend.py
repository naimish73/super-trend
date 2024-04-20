# Import necessary libraries
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt  # Example plotting library
from yfinance import Ticker
import numpy as np

# Define symbol and timeframe
symbol = "TCS.NS"

# Global variable to keep track of whether the full day's data has been fetched
has_fetched_full_day_data = False
symbol_data = pd.DataFrame()

def fetch_live_data(symbol):
    global has_fetched_full_day_data, symbol_data
    if has_fetched_full_day_data:
        # Fetch the full day's data and select the last row
        latest_data = Ticker(symbol).history(interval="1m", period='1m')
        latest_data = latest_data.iloc[-1:]
        # print('latest_data:', latest_data)
        # Concatenate the latest minute's data with the existing DataFrame
        symbol_data = pd.concat([symbol_data, latest_data])
    else:
        # Fetch the full day's data
        symbol_data = Ticker(symbol).history(interval="1m", period='1d')
        has_fetched_full_day_data = True

    # print('\n\nlive data:\n', symbol_data)
    symbol_data.to_csv('dataset/symbol_data.csv')
    return symbol_data

# Function to calculate the SuperTrend
def calculate_supertrend(data):
    atrPeriod = 20  # ATR Length
    factor = 2.0    # Factor

    # Calculate SuperTrend
    # super_trend, direction = ta.supertrend(data['High'], data['Low'], data['Close'], atrPeriod, factor)
    super_trend = ta.supertrend(data['High'], data['Low'], data['Close'], atrPeriod, factor)
    print('super_trend:', super_trend)

    # Adjust for backtesting purposes
    super_trend = super_trend.shift(1)

    # Save the SuperTrend values to a CSV file
    # super_trend_df = pd.DataFrame({'SuperTrend': super_trend, 'Direction': direction}, index=data.index)
    super_trend.to_csv('dataset/super_trend.csv')

    return super_trend


# Function to plot the SuperTrend and symbol data together
def plot_supertrend_with_symbol_data(super_trend, symbol_data):
    fig, ax1 = plt.subplots()

    # for index, row in super_trend.iterrows():
    #     print(index, row['SUPERTd_7_2.0'])

    ax1.plot(super_trend.index, super_trend['SUPERTl_20_2.0'], label="Supertrend", color='green')
    ax1.plot(super_trend.index, super_trend['SUPERTs_20_2.0'], label="Supertrend", color='red')

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
    plt.show(block=True)
    # plt.pause()
    # plt.close()

# Main function to start the live plotting
def main(symbol):
    # while True:
    data = fetch_live_data(symbol)
    super_trend = calculate_supertrend(data)
    plot_supertrend_with_symbol_data(super_trend, data)

# Start the live plotting
main(symbol)

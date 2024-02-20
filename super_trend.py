# Import necessary libraries
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt  # Example plotting library
from yfinance import Ticker

# Define symbol and timeframe
symbol = "TCS.NS"

# Global variable to keep track of whether the full day's data has been fetched
has_fetched_full_day_data = False
symbol_data = pd.DataFrame()

def fetch_live_data(symbol):
    global has_fetched_full_day_data, symbol_data
    if has_fetched_full_day_data:
        # Fetch the full day's data and select the last row
        latest_data = Ticker(symbol).history(interval="1m", period="1d").iloc[-1:]
        # Concatenate the latest minute's data with the existing DataFrame
        symbol_data = pd.concat([symbol_data, latest_data])
    else:
        # Fetch the full day's data
        symbol_data = Ticker(symbol).history(interval="1m", period="1d")
        has_fetched_full_day_data = True

    print('\n\nlive data:\n', symbol_data)
    return symbol_data

# Function to calculate the SuperTrend
def calculate_supertrend(data):
    super_trend = data.ta.supertrend()
    print('\n\nSuper Trend:\n', super_trend)
    return super_trend

# Function to plot the SuperTrend and symbol data together
def plot_supertrend_with_symbol_data(super_trend, symbol_data):
    fig, ax1 = plt.subplots()

    # Plotting SuperTrend
    ax1.plot(super_trend.index, super_trend["SUPERT_7_3.0"], label="Supertrend", color='blue')
    ax1.set_ylabel('Supertrend', color='blue')
    ax1.tick_params('y', colors='blue')

    # Creating a second y-axis for symbol data
    ax2 = ax1.twinx()
    ax2.plot(symbol_data.index, symbol_data["Close"], label="Close", color='red')  # Example: Close price
    ax2.set_ylabel('TCS Current Prize', color='red')
    ax2.tick_params('y', colors='red')

    fig.tight_layout()
    plt.ion()
    plt.legend()
    plt.show()
    plt.pause(60)
    plt.close()

# Main function to start the live plotting
def main(symbol):
    while True:
        data = fetch_live_data(symbol)
        super_trend = calculate_supertrend(data)
        plot_supertrend_with_symbol_data(super_trend, data)

# Start the live plotting
main(symbol)

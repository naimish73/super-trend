from yfinance import Ticker
import pandas_ta as ta
import numpy as np
import pandas as pd


# Fetch the latest minute's data
def fetch_realtime_data(symbol):
    latest_data = Ticker(symbol).history(interval="1m", period='1d')
    return latest_data


# Calculate superternd
def calculate_supertrend(data):
    super_trend = ta.supertrend(data['High'], data['Low'], data['Close'], factor=20, atrPeriod=2)
    return super_trend


# Checking the range of the prize with super-trend
def check_supertrend_range(data, super_trend):
    # prize_range_touch = []

    for i in range(int(data.shape[0])):
        if data.isnull().iloc[i,3] or super_trend.isnull().iloc[i,0]:
            continue
        
        if int(super_trend.iloc[i,1]) == -1:
            supertrend_line = 3
        elif int(super_trend.iloc[i,1]) == 1:
            supertrend_line = 2
        else:
            supertrend_line = np.nan
            
        rangeDifference = data.iloc[i,3] * 0.01
        if abs(data.iloc[i, 3] - super_trend.iloc[i, supertrend_line]) < rangeDifference:
            # prize_range_touch.append(data.iloc[i, 3])
            print('close_prize:', data.iloc[i, 3], ', super_trend:', super_trend.iloc[i, supertrend_line], 'range_difference:', abs(data.iloc[i, 3] - super_trend.iloc[i, supertrend_line]))
            return True
    
    return False
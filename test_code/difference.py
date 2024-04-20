from yfinance import Ticker
import pandas_ta as ta
import numpy as np

# Define symbol
symbol = "TCS.NS"
rangeDifference = 300
check = False
prize_range_touch = []

def fetch_realtime_data(symbol):
    # Fetch the latest minute's data
    latest_data = Ticker(symbol).history(interval="1d", start="2023-01-02", end="2024-02-19")
    # print('latest data: ', latest_data)
    return latest_data

def calculate_supertrend(data):
    super_trend = ta.supertrend(data['High'], data['Low'], data['Close'], atr=20, multiplier=2)
    super_trend.to_csv('dataset/super_trend.csv')
    # print('\n\nSuper Trend:\n', super_trend)
    return super_trend

def check_supertrend_range(data, super_trend):
    # supertrend_line = "SUPERTl_7_2.0" if super_trend["SUPERTd_7_2.0"].iloc[-1] == 1 else "SUPERTs_7_2.0"
    # if super_trend["SUPERTd_7_2.0"].iloc[-1] == -1:
    #     supertrend_line = "SUPERTs_7_2.0"

    # super_trend[supertrend_line] = super_trend['SUPERTs_7_2.0']
    
    if int(super_trend["SUPERTd_7_2.0"].iloc[-1]) == -1:
        supertrend_line = "SUPERTs_7_2.0"
    elif int(super_trend["SUPERTd_7_2.0"].iloc[-1]) == 1:
        supertrend_line = "SUPERTl_7_2.0"
    else:
        supertrend_line = "SUPERTs_7_2.0"  # Append other values here

    # supertrend_line = "SUPERTs_7_2.0"

    for i in range(int(data.shape[0])):
        if data['Close'].isnull().values.any() or super_trend['SUPERT_7_2.0'].isnull().values.any():
            print('Nan found', data.index[i])
        if np.isnan(data['Close'].iloc[i]) or np.isnan(super_trend['SUPERT_7_2.0'].iloc[i]):
            continue 
        # for value in supertrend_line:
        #     print('supertrend_line:', value)
        
        if abs(data['Close'].iloc[i] - super_trend[supertrend_line].iloc[i]) < rangeDifference:
            prize_range_touch.append(data['Close'])
            check = True

def main(symbol):
    # Fetch real-time data
    data = fetch_realtime_data(symbol)
    print('\ndata fetched')
    
    # Calculate SuperTrend
    super_trend = calculate_supertrend(data)
    print('\nSuperTrend calculated')
    
    # Check if SuperTrend falls within a certain range
    check_supertrend_range(data, super_trend)
    # if check:
    #     print('\nWithin the range')
    # else:
    #     print('\nNot within the range')
    # print('\n\nprize_range_touch:', prize_range_touch)


if __name__ == "__main__":
    main(symbol)

import pandas as pd
import pandas_ta as ta
import yfinance as yf
import datetime as dt
import streamlit as st
import plotly.graph_objects as go
from symbolList import symbol_list
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(page_title="Stock Price Analysis", page_icon="📈", layout="wide")

def fetch_data(symbol, timeframe, period):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=timeframe)
    supertrend = df.ta.supertrend(length=20, multiplier=2.0)

    if period == "6mo" and timeframe == "1d":
        df.reset_index(inplace=True)
        df.rename(columns={'Date': 'Datetime'}, inplace=True)
        supertrend.reset_index(inplace=True)
        supertrend.rename(columns={'Date': 'Datetime'}, inplace=True)

    supertrend.reset_index(inplace=True)
    merged_df = pd.merge(df, supertrend, on="Datetime")
    return merged_df

# def check_supertrend_range(merge_data):
#     for i in range(int(merge_data.shape[0])):
#         if merge_data.isnull().iloc[i, 4] or merge_data.isnull().iloc[i, 8]:
#             continue
        
#         if int(merge_data.iloc[i, 9]) == -1:
#             supertrend_line = 11
#         elif int(merge_data.iloc[i, 9]) == 1:
#             supertrend_line = 10
#         else:
#             supertrend_line = np.nan
            
#         rangeDifference = merge_data.iloc[i, 4] * 0.01

#         if abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) < rangeDifference:
#             print('Date', merge_data.iloc[i, 0], 'close_prize:', merge_data.iloc[i, 4], ', super_trend:', merge_data.iloc[i, supertrend_line], 'range_difference:', abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]))
#             return True
    
#     return False

import numpy as np

def check_supertrend_range(merge_data):
    for i in range(int(merge_data.shape[0])):
        if merge_data.isnull().iloc[i, 4] or merge_data.isnull().iloc[i, 8]:
            continue
        
        supertrend_value = merge_data.iloc[i, 9]
        if not np.isnan(supertrend_value):  # Check if supertrend_value is not NaN
            if int(supertrend_value) == -1:
                supertrend_line = 11
            elif int(supertrend_value) == 1:
                supertrend_line = 10
            else:
                supertrend_line = np.nan
            
            if not np.isnan(supertrend_line):  # Check if supertrend_line is a valid index
                rangeDifference = merge_data.iloc[i, 4] * 0.01

                if abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) < rangeDifference:
                    print('Date', merge_data.iloc[i, 0], 'close_prize:', merge_data.iloc[i, 4], ', super_trend:', merge_data.iloc[i, supertrend_line], 'range_difference:', abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]))
                    return True
    
    return False

def plot_graph(df):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=df['Datetime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='market data'))
    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['SUPERTl_20_2.0'], name='Supertrend Long', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['SUPERTs_20_2.0'], name='Supertrend Short', line=dict(color='red')))
    fig.update_layout(
        title='Stock Price with Supertrend', 
        xaxis_title='Datetime', 
        yaxis_title='Price',
        width=1500, 
        height=500,
        template='plotly_dark',  
    )

    fig.update_traces(
        line=dict(width=1),
    )

    st.plotly_chart(fig)

import logging

logging.basicConfig(level=logging.INFO)

def show_filtered_stocks(symbol, tf, pr):
    logging.info(f"Fetching data for symbol: {symbol}")
    df = fetch_data(symbol, tf, pr)
    logging.info(f"Fetched data for symbol: {symbol}")

    logging.info(f"Checking Supertrend range for symbol: {symbol}")
    check_range = check_supertrend_range(df)
    logging.info(f"Checked Supertrend range for symbol: {symbol}")

    if check_range:
        logging.info(f"Plotting graph for symbol: {symbol}")
        with st.expander(f"{symbol}"):
            plot_graph(df)
        logging.info(f"Plotted graph for symbol: {symbol}")
    else:
        logging.info(f"No Supertrend range found for symbol: {symbol}")

def app():
    Timeframe = ["1m", "5m", "15m", "1d"]
    period = ['1d', '5d', '1mo', '6mo']
    tf, pr, save = st.columns(3)
    tf = tf.selectbox("Select Timeframe", Timeframe)
    pr = pr.selectbox("Select Period", period)
    save.text("Save")
    save = save.button("Save")

    if pr == "6mo" and tf != "1d":
        st.warning("Timeframe should be 1d for 6 months period")
        tf = "1d"

    if save:
        start_time = dt.datetime.now()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            symbol_list_values = list(symbol_list.values())[:4]  # Convert to list and slice
            for symbol in symbol_list_values:
                futures.append(executor.submit(show_filtered_stocks, symbol, tf, pr))
            for future in as_completed(futures):
                future.result()
        end_time = dt.datetime.now()
        print(f"Time taken: {(end_time - start_time).total_seconds()} seconds")

if __name__ == "__main__":
    app()

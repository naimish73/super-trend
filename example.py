import pandas as pd
import streamlit as st
import numpy as np
import yfinance as yf
import pandas_ta as ta
# Assuming you have symbol_list and other relevant data ready
from symbolList import symbol_list

st.set_page_config(page_title="Stock Price Analysis", page_icon="📈", layout="wide")

symbol_list = {
    "Infosys Limited": "INFY.NS",
    "Deepak Nitrite Limited": "DEEPAKNTR.NS",
    "Delta Corp Limited": "DELTACORP.NS",
    "Divis Laboratories Limited": "DIVISLAB.NS",
    "Dixon Technologies (India) Limited": "DIXON.NS",
    
}
name = []
sup_trend = []
close_price = []
filtered_data = []
range_diffrence = []
range_abs_difference = []
chart_links = []  # List to hold TradingView chart links

def Fetch_data(symbol, timeframe, period):

    if timeframe == "1m":
        if period in ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]:
            st.warning(f"{timeframe} time frame is only for 7 days period")
            return pd.DataFrame()

    if timeframe in ["5m", "15m", "30m"]:
        if period in ["3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]:
            st.warning(f"{timeframe} time frame is only for 60 days period")
            return pd.DataFrame()

    if timeframe == "1h":
        if period in ["5y", "10y", "ytd", "max"]:
            st.warning(f"{timeframe} time frame is only for 2 years period")
            return pd.DataFrame()

    if (timeframe == "30m" and period == "1d") or \
       (timeframe == "1h" and period == "1d") or \
       (timeframe == "1d" and period == "1d") or \
       (timeframe == "1d" and period == "5d"):
        st.info(f"Due to some technical issues, {timeframe} timeframe and {period} period is not available for now !!!")
        return pd.DataFrame()
    
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=timeframe)

    supertrend = df.ta.supertrend(length=20,multiplier=2.0)

    supertrend.reset_index(inplace=True)
    df.reset_index(inplace=True)

    if (timeframe == "30m" and period=="1d") or (timeframe == "1h" and period=="1d") or (timeframe == "1d" and period=="1d") or (timeframe == "1d" and period=="5d") :
        st.info(f"Duo to some Technical issue , {timeframe} and {period} is not available for now !!!")
        return pd.DataFrame()

    if period == "6mo" and timeframe == "1d":
        df.rename(columns={'Date': 'Datetime'}, inplace=True)
        supertrend.rename(columns={'Date': 'Datetime'}, inplace=True)

    try:
        merged_df = pd.merge(df, supertrend, on="Datetime")
    except:
        try:
            df.rename(columns={'Date': 'Datetime'}, inplace=True)    
            supertrend.rename(columns={'Date': 'Datetime'}, inplace=True)    

            merged_df = pd.merge(df, supertrend, on="Datetime")
        except:
            pass

    return merged_df


def check_supertrend_range(merge_data,Name,symbol):
    # prize_range_touch = []
    # print(merge_data.columns)
    # print(merge_data)
    
    for i in range(int(merge_data.shape[0])):
        if merge_data.isnull().iloc[i,4] or merge_data.isnull().iloc[i,9]:
            continue    
        
        # print('data: ', merge_data.iloc[i,9])
        if int(merge_data.iloc[i,9]) == -1:
            supertrend_line = 11
        elif int(merge_data.iloc[i,9]) == 1:
            supertrend_line = 10
        else:
            supertrend_line = np.nan
            
        rangeDifference = merge_data.iloc[i,4] * 0.01
        # print('range_difference:', rangeDifference)
        # print(supertrend_line, merge_data.iloc[i, supertrend_line], type(supertrend_line))
        # print('abs :',abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) )

        # st.write(supertrend_line)
        if supertrend_line == np.nan: continue
        range_abs_diff = abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line])
        if  range_abs_diff  < rangeDifference :
            
            name.append(Name)
            sup_trend.append(merge_data.iloc[i, supertrend_line])
            close_price.append(merge_data.iloc[i, 4])
            filtered_data.append(merge_data.iloc[i,0])
            range_diffrence.append(rangeDifference)
            range_abs_difference.append(range_abs_diff)

            # Construct TradingView chart link
            symbol = symbol.split(".")[0]
            chart_link = f"https://www.tradingview.com/chart/?symbol=NSE:{symbol}&interval=1&range=1&style=1&timezone=Asia%2FKolkata&theme=dark&studies=%5B%5D&study1=SuperTrend&interval=1&range=1"
            chart_links.append(chart_link)


            print(Name,'Date',merge_data.iloc[i,0],'close_prize:', merge_data.iloc[i, 4], 'super_trend:', merge_data.iloc[i, supertrend_line], 'range_difference:', range_abs_diff)
            return True
        
    return False

def show_filtered_stocks(company_name,symbol,tf,pr):
    df=Fetch_data(symbol,timeframe=tf, period=pr)
    if len(df) != 0:
        check_range = check_supertrend_range(df,company_name,symbol)

      
    else:
        st.stop()

def Find_Company_name(symbol):
    symbol= symbol + ".NS"
    for key, value in symbol_list.items():
        if value == symbol:
            return key

def app():
    Timeframe = ["1m", "5m", "15m", "30m", "1h", '1d']
    period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    tf, pr = st.columns(2)
    tf = tf.selectbox("Select Timeframe", Timeframe)
    pr = pr.selectbox("Select Period", period)
    save = st.button("Scan")

    if period == "6mo":
        if Timeframe != "1d":
            st.warning("Timeframe should be 1d for 6 months period")
            Timeframe = "1d"

    if save:
        with st.spinner("Fetching data ..."):
            for Company_name, symbol in symbol_list.items():
                show_filtered_stocks(Company_name, symbol, tf, pr)

        data = {
            'Company Name': name,
            'Date': filtered_data,
            'Close Price': close_price,
            'Supertrend': sup_trend,
            'Range Difference': range_diffrence,
            'Range Abs Difference': range_abs_difference,
            'TradingView Chart': chart_links  # Adding TradingView chart links to the data
        }
        df = pd.DataFrame(data)
        

        st.data_editor(
            df,
            column_config={
                # "Company Name": st.column_config.LinkColumn(
                #     validate="TradingView Chart",
                #     help="Click to view TradingView chart"
                    
                # ),
                 "TradingView Chart": st.column_config.LinkColumn(
                    validate="TradingView Chart",
                    help="Click to view TradingView chart",
                    display_text="Open Chart"
                )
            },
            hide_index=True
        )

if __name__ == "__main__":
    app()

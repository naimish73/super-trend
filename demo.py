import pandas as pd
import pandas_ta as ta
import yfinance as yf
import datetime as dt
import pandas_ta as ta
import streamlit as st
import plotly.graph_objects as go
from  symbolList import symbol_list
import numpy as np

st.set_page_config(page_title="Stock Price Analysis", page_icon="📈", layout="wide")

# symbol_list = {
#     "Aditya Birla Capital Limited": "ABCAPITAL.NS",
#     "Indus Towers Limited": "INDUSTOWER.NS",
#     "Infosys Limited": "INFY.NS",
# }
# st.session_state['s']= 0
# if st.session_state.s==0:
#     st.session_state.s+=1
#     try:
#         stocks= sl.symbol_list
#         companies = stocks.keys()
#     except:
#         st.write("Error in fetching data from database")
#         st.stop()

# company=st.selectbox("Select Company",companies)
# symbol = stocks.get(company)x

# st.write(f"Selected Company: {company}")

# with st.sidebar:
#     st.sidebar.markdown(' # Stock Price Analysis ')
#     st.sidebar.title(f"Welcome ")
#     dtnow = dt.datetime.now()
        
#     DAY = dtnow.strftime('%A')
   
#     if DAY == 'Saturday' or DAY == 'Sunday':
#         start_date =  dtnow.today() - dt.timedelta(days=3)    
#         end_date = dtnow.today() - dt.timedelta(days=2)
#     else:
#         start_date = dtnow.today()
#         end_date = dtnow.today() + dt.timedelta(days=1)

#     start_date = st.sidebar.date_input("start date", start_date)
#     end_date = st.sidebar.date_input("End date",end_date)

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

def check_supertrend_range(merge_data):
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
        if  abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) < rangeDifference :
            # prize_range_touch.append(data.iloc[i, 3])
            print('Date',merge_data.iloc[i,0],'close_prize:', merge_data.iloc[i, 4], ', super_trend:', merge_data.iloc[i, supertrend_line], 'range_difference:', abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]))
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

    # Modify candlestick style to Yahoo Finance style
    fig.update_traces(
        line=dict(width=1),            # Width of scatter plot lines
    )


    st.plotly_chart(fig)


def show_filtered_stocks(symbol,tf,pr):
    df=Fetch_data(symbol,timeframe=tf, period=pr)
    if len(df) != 0:
        check_range = check_supertrend_range(df)

        if check_range:
            
            with st.expander(f"{symbol}"):
                plot_graph(df)
    else:
        st.stop()
                
    
def app():
    Timeframe = ["1m", "5m", "15m", "30m", "1h",'1d']
    period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    tf,pr=st.columns(2)
    tf = tf.selectbox("Select Timeframe", Timeframe)
    pr = pr.selectbox("Select Period", period)
    save = st.button("scan")

    if period == "6mo":
        if Timeframe != "1d":
            st.warning("Timeframe should be 1d for 6 months period")
            Timeframe= "1d"

    if save:
        with st.spinner("Fetching data ..."):
            for symbol in symbol_list.values():

                show_filtered_stocks(symbol,tf,pr)
   
    # st.table(df)

if __name__ == "__main__":
    app()


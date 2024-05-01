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
# symbol = stocks.get(company)

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
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=timeframe)
    supertrend = df.ta.supertrend(length=20,multiplier=2.0)

    if period == "6mo" and timeframe == "1d":
        df.reset_index(inplace=True)
        df.rename(columns={'Date': 'Datetime'}, inplace=True)
        supertrend.reset_index(inplace=True)
        supertrend.rename(columns={'Date': 'Datetime'}, inplace=True)

        # st.write(supertrend)
        # st.write(df)
        # merged_df = pd.merge(df, supertrend, on="Date")

    if timeframe == "30m":
        pass
        # st.write(df.columns)
        # # df.drop(columns=["Open_y", "High_y", "Low_y", "Close_y", "Volume_y", "Dividends_y", "Stock Splits_y"],axis=1, inplace=True)

        # df.rename(columns={
        #     "Open x": "Open",
        #     "High x": "High",
        #     "Low x": "Low",
        #     "Close x": "Close",
        #     "Volume x": "Volume",
        #     "Dividends x": "Dividends",
        #     "Stock Splits x": "Stock Splits",
        # }, inplace=True)
  
    # supertrend.reset_index(inplace=True)
    # st.write(supertrend)
    # st.write(df)
    merged_df = pd.merge(df, supertrend, on="Datetime")
    # st.write(merged_df)
    return merged_df

def check_supertrend_range(merge_data):
    # prize_range_touch = []
    # print(merge_data.head())
    
    for i in range(int(merge_data.shape[0])):
        if merge_data.isnull().iloc[i,4] or merge_data.isnull().iloc[i,8]:
            continue
        
        if int(merge_data.iloc[i,9]) == -1:
            supertrend_line = 11
        elif int(merge_data.iloc[i,9]) == 1:
            supertrend_line = 10
        else:
            supertrend_line = np.nan
            
        rangeDifference = merge_data.iloc[i,4] * 0.01
        # print('range_difference:', rangeDifference)

        # print('abs :',abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) )

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

# def plot_graph():
#     fig = go.Figure()

#     # Candlestick trace
#     fig.add_trace(go.Candlestick(x=df['Datetime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='market data'))
    
#     # Supertrend Long trace
#     fig.add_trace(go.Scatter(x=df['Datetime'], y=df['SUPERTl_20_2.0'], name='Supertrend Long', line=dict(color='green')))
    
#     # Supertrend Short trace
#     fig.add_trace(go.Scatter(x=df['Datetime'], y=df['SUPERTs_20_2.0'], name='Supertrend Short', line=dict(color='red')))
    
#     # Add buy tag at the starting point of each green line
#     green_start_indices = df[df['SUPERTl_20_2.0'].diff() > 0].index
#     for green_start_index in green_start_indices:
#         fig.add_annotation(x=df.loc[green_start_index, 'Datetime'], y=df.loc[green_start_index, 'Low'], text="Buy", showarrow=True, arrowhead=1, ax=0, ay=-40, bgcolor='green')

#     # Add sell tag at the starting point of red line if available
#     red_start_indices = df[df['SUPERTs_20_2.0'].diff() > 0].index
#     if len(red_start_indices) > 0:
#         red_start_index = red_start_indices[0]
#         fig.add_annotation(x=df.loc[red_start_index, 'Datetime'], y=df.loc[red_start_index, 'High'], text="Sell", showarrow=True, arrowhead=1, ax=0, ay=-40)
    
#     fig.update_layout(
#         title='Stock Price with Supertrend', 
#         xaxis_title='Datetime', 
#         yaxis_title='Price',
#         width=1750, 
#         height=800,
#         template='plotly_dark',  
#     )

#     # Modify candlestick style to Yahoo Finance style
#     fig.update_traces(
#         line=dict(width=1),            # Width of scatter plot lines
#     )

#     st.plotly_chart(fig)


def show_filtered_stocks(symbol,tf,pr):
    df=Fetch_data(symbol,tf, pr)
    check_range = check_supertrend_range(df)

    if check_range:
        
        with st.expander(f"{symbol}"):
            plot_graph(df)
    
def app():
    Timeframe = ["1m", "5m", "15m",'1d']#, "30m", "1h"]
    period = ['1d', '5d', '1mo','6mo']#, '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    tf,pr,save=st.columns(3)
    tf = tf.selectbox("Select Timeframe", Timeframe)
    pr = pr.selectbox("Select Period", period)
    save.text("Save")
    save = save.button("Save")

    if period == "6mo":
        if Timeframe != "1d":
            st.warning("Timeframe should be 1d for 6 months period")
            Timeframe= "1d"

    if save:
        for symbol in symbol_list.values():

            show_filtered_stocks(symbol,tf,pr)
   
    # st.table(df)

app()


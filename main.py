import pandas as pd
import pandas_ta as ta
import yfinance as yf
import datetime as dt
import pandas_ta as ta
import streamlit as st
import plotly.graph_objects as go
import symbolList as sl

st.session_state['s']= 0
if st.session_state.s==0:
    st.session_state.s+=1
    try:
        stocks= sl.symbol_list
        companies = stocks.keys()
    except:
        st.write("Error in fetching data from database")
        st.stop()

company=st.selectbox("Select Company",companies)
symbol = stocks.get(company)

st.write(f"Selected Company: {company}")

with st.sidebar:
    st.sidebar.markdown(' # Stock Price Analysis ')
    st.sidebar.title(f"Welcome ")
    dtnow = dt.datetime.now()
        
    DAY = dtnow.strftime('%A')
   
    if DAY == 'Saturday' or DAY == 'Sunday':
        start_date =  dtnow.today() - dt.timedelta(days=3)    
        end_date = dtnow.today() - dt.timedelta(days=2)
    else:
        start_date = dtnow.today()
        end_date = dtnow.today() + dt.timedelta(days=1)

    start_date = st.sidebar.date_input("start date", start_date)
    end_date = st.sidebar.date_input("End date",end_date)

def Fetch_data(symbol, timeframe, start_date, end_date):
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date, interval=timeframe)

    supertrend = df.ta.supertrend(length=20, multiplier=2.0)
    df.reset_index(inplace=True)
    supertrend.reset_index(inplace=True)

    merged_df = pd.merge(df, supertrend, on="Datetime")

    return merged_df

df=Fetch_data(symbol,"1m", start_date, end_date)
st.write(df)

def plot_graph():
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['Close'], name='Close', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['SUPERTl_20_2.0'], name='Supertrend Long', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['SUPERTs_20_2.0'], name='Supertrend Short', line=dict(color='red')))
    fig.update_layout(title='Stock Price with Supertrend', xaxis_title='Datetime', yaxis_title='Price', width=1000, height=500)

    st.plotly_chart(fig)

plot_graph()


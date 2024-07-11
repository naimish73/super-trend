import pandas as pd
import pandas_ta as ta
import yfinance as yf
import pandas_ta as ta
import streamlit as st
import plotly.graph_objects as go
import symbolList as sl

st.session_state["s"] = 0
if st.session_state.s == 0:
    st.session_state.s += 1
    try:
        stocks = sl.symbol_list
        companies = stocks.keys()
    except:
        st.write("Error in fetching data from database")
        st.stop()

company = st.selectbox("Select Company", companies)
symbol = stocks.get(company)

st.write(f"Selected Company: {company}")


def Fetch_data(symbol, timeframe="1d"):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="6mo", interval=timeframe)

    supertrend = df.ta.supertrend(length=20, multiplier=2.0)
    df.reset_index(inplace=True)
    supertrend.reset_index(inplace=True)

    merged_df = pd.merge(df, supertrend, on="Date")

    return merged_df


df = Fetch_data(symbol)
st.write(df)


def plot_graph():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df["Date"], y=df["Close"], name="Close", line=dict(color="blue"))
    )
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SUPERTl_20_2.0"],
            name="Supertrend Long",
            line=dict(color="green"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SUPERTs_20_2.0"],
            name="Supertrend Short",
            line=dict(color="red"),
        )
    )
    fig.update_layout(
        title="Stock Price with Supertrend",
        xaxis_title="Date",
        yaxis_title="Price",
        width=1000,
        height=500,
    )

    st.plotly_chart(fig)


plot_graph()

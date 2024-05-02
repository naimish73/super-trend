import streamlit as st
import pandas as pd

from highLow import get52WeekHighLow

# Main function to run the Streamlit web app
def main():
    st.title('52 Week High Low stocks')

    if st.button('Fetch'):
        with st.spinner('Fetching data...'):
            stocks_52_week_high, stocks_52_week_low = get52WeekHighLow()

        # Display section for 52-week highs
        st.header('52 Week Highs')
        st.write(stocks_52_week_high)
        
        # Display section for 52-week lows
        st.header('52 Week Lows')
        st.write(stocks_52_week_low)

# Run the app
if __name__ == '__main__':
    main()

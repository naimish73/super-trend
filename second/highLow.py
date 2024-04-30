import yfinance as yf
import datetime as dt

# import os
# import sys
# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# sys.path.append(parent_dir)
# from symbolList import symbol_list

symbol_list = {
        # "Mahindra & Mahindra Limited": "M&M.NS",
        # "Ashok Leyland Limited": "ASHOKLEY.NS",
        # "Astral Limited": "ASTRAL.NS",
        # "Aarti Industries Limited": "AARTIIND.NS",
        # "ABB Limited": "ABB.NS",
        # "Abbott India Limited": "ABBOTINDIA.NS",
        "Kotak Mahindra Bank Limited": "KOTAKBANK.NS",
}

def get_high_low(symbol):
    ticker = yf.Ticker(symbol)
    # Fetching fundamental data
    fundamental_data = ticker.info

    # Extracting 52-week high and low
    week_high = fundamental_data.get('fiftyTwoWeekHigh')
    week_low = fundamental_data.get('fiftyTwoWeekLow')

    return week_high, week_low

def compare_today_price(symbol, week_high, week_low):
    try:
        ticker = yf.Ticker(symbol)
        today_data = ticker.history(interval="1m", period='1d')
        # print(today_data)
        highest_close = today_data['Close'].max()
        lowest_close = today_data['Close'].min()
        one_percent = 0.01 * today_data['Close'].tail(1).values[0]

        print('\nstock name:', symbol)
        print('highest_close:', highest_close)
        print('lowest_close:', lowest_close)
        print('\nweek_high:', week_high)
        print('week_low:', week_low, end='\n\n')

        print('abs(highest_close - week_high):', abs(highest_close - week_high))
        print('abs(lowest_close - week_low):', abs(lowest_close - week_low))
        print('0.01 * today_data[Close]:', 0.01 * today_data['Close'].tail(1).values[0])

        if highest_close >= week_high or abs(highest_close - week_high) < one_percent:
            return "52 Week High"
        elif lowest_close <= week_low or abs(lowest_close - week_low) < one_percent:
            return "52 Week Low"
        else:
            return "Neither 52 Week High nor 52 Week Low"
    except Exception as e:
        print(f'Error in stock {symbol_list[symbol]}:', e)
        pass

def main():
    stocks_52_week_high = []
    stocks_52_week_low = []

    for company, symbol in symbol_list.items():
        week_high, week_low = get_high_low(symbol)
        status = compare_today_price(symbol, week_high, week_low)

        if status == "52 Week High":
            stocks_52_week_high.append(company)
        elif status == "52 Week Low":
            stocks_52_week_low.append(company)

    print("Stocks at 52 Week High today:")
    print(stocks_52_week_high)
    print("\nStocks at 52 Week Low today:")
    print(stocks_52_week_low)

if __name__ == "__main__":
    main()

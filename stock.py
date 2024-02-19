import yfinance as yf
import pandas as pd

symbol = "TCS.NS"
start_date = '2023-01-01'
end_date = '2024-02-19'

data = yf.download(symbol, start=start_date, end=end_date)

data.index.name = 'Date'
data.index = pd.to_datetime(data.index)

file_name = f"tcs_stock_{start_date}_{end_date}"

try:
    data.to_csv(file_name, index=True)
    print(f"{file_name} data downloaded successfully")
except Exception as e:
    print(f'Error in saving data, {e}')

print(data)
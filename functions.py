from yfinance import Ticker
import pandas_ta as ta
import numpy as np
import pandas as pd
# from symbolList import symbol_list

symbol_list = {
    "Aarti Industries Limited": "AARTIIND.NS",
}

# Fetch the latest minute's data
def fetch_realtime_data(symbol):
    latest_data = Ticker(symbol).history(interval="1m", period='1d')
    return latest_data


# Calculate superternd
def calculate_supertrend(data):
    super_trend = data.ta.supertrend(length=20, multiplier=2.0)

    data.reset_index(inplace=True)
    super_trend.reset_index(inplace=True)
    try:
        merged_df = pd.merge(data, super_trend, on="Datetime")
        merged_df.to_csv('super-trend/dataset/merged_df.csv')

    except Exception as e:
        print(e)
        return None
    # print([[merged_df['Datetime'], merged_df['Close'],merged_df['SUPERT_20_2.0'],merged_df['SUPERTl_20_2.0'] , merged_df['SUPERTd_20_2.0']]])
    
    return merged_df


# Checking the range of the prize with super-trend
def check_supertrend_range(merge_data):
    # prize_range_touch = []

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
        print('range_difference:', rangeDifference)

        print('abs :',abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) )

        if abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]) < rangeDifference:
            # prize_range_touch.append(data.iloc[i, 3])
            print('close_prize:', merge_data.iloc[i, 4], ', super_trend:', merge_data.iloc[i, supertrend_line], 'range_difference:', abs(merge_data.iloc[i, 4] - merge_data.iloc[i, supertrend_line]))
            return True
    
    return False

def check_supertrend_range2(merge_data):

    print(merge_data.head())

if __name__ == '__main__':
    # prize_range_touch = []

    for name, sbl in symbol_list.items():
        data = fetch_realtime_data(sbl)
        merged_data = calculate_supertrend(data)
        check_range = check_supertrend_range2(merged_data)
        

    #     if check_range:
    #         prize_range_touch.append(name)

    # if len(prize_range_touch) > 0:
    #     print(prize_range_touch)
    
    
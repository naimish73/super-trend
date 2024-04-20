#For Complete Algomojo Python Documentation Visit - https://pypi.org/project/algomojo/
#Coded by Rajandran R - www.marketcalls.in / www.algomojo.com

from algomojo.pyapi import *
from datetime import datetime

import yfinance as yf

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import math
import time
import threading

#set the StrategyName, broker code, Trading symbol, exchange, product and quantity
strategy = "Supertrend Python"
broker = "an"
api_key = "46ad9245cca3dfe957deb235a39d02a3"
api_secret = "30ca108cfb91f458babd2681fb6d0817"
symbol = "RELIANCE-EQ"  #Trading Symbol
exchange = "NSE"
product="MIS"
quantity = 10


#yfinance datafeed settings
yfsymbol = "RELIANCE.NS" #Datafeed Symbol
period = "1d"
timeframe = "1m"

#supertrend indicator inputs
atr_period = 5
atr_multiplier = 1.0

# Set the API Key and API Secret key obtained from Algomojo MyAPI Section
algomojo = api(api_key=api_key, api_secret=api_secret)


def Supertrend(df, atr_period, multiplier):
    
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    # calculate ATR
    price_diffs = [high - low, 
                   high - close.shift(), 
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    # default ATR calculation in supertrend indicator
    atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean() 
    # df['atr'] = df['tr'].rolling(atr_period).mean()
    
    # HL2 is simply the average of high and low prices
    hl2 = (high + low) / 2
    # upperband and lowerband calculation
    # notice that final bands are set to be equal to the respective bands
    final_upperband = upperband = hl2 + (multiplier * atr)
    final_lowerband = lowerband = hl2 - (multiplier * atr)
    
    # initialize Supertrend column to True
    supertrend = [True] * len(df)
    
    for i in range(1, len(df.index)):
        curr, prev = i, i-1
        
        # if current close price crosses above upperband
        if close[curr] > final_upperband[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]
            
            # adjustment to the final bands
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        # to remove bands according to the trend direction
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan
    
    return pd.DataFrame({
        'Supertrend': supertrend,
        'Final Lowerband': final_lowerband,
        'Final Upperband': final_upperband
    }, index=df.index)
    
    






def supertrend_strategy():
    # Get historical data for the stock using Yahoo Finance API
    stock = yf.Ticker(yfsymbol)
   
     # Set initial values for variables
    position = 0
    
    


    # Main loop
    while True:
        # Get historical price data from 5min timeframe 

        df = stock.history(period=period, interval=timeframe)
        close = df.Close.round(2)
        supertrend = Supertrend(df, atr_period, atr_multiplier)
       

        # Calculate Supertrend
        is_uptrend = supertrend['Supertrend']

        # Determine the crossover point
        longentry = is_uptrend[-2] and (not is_uptrend[-3])
        shortentry = is_uptrend[-3] and (not is_uptrend[-2])

        
        # Place an order if there's a crossover and we don't already have a position
        if longentry and position<=0:

            # Update position variable
            position = quantity

            # Place Smart market buy order
            response = algomojo.PlaceSmartOrder(broker=broker ,
                                strategy=strategy,
                                exchange=exchange,
                                symbol=symbol,
                                action="BUY",
                                product=product,
                                pricetype="MARKET",
                                quantity=quantity,
                                price="0",
                                position_size=position,
                                trigger_price="0",
                                disclosed_quantity="0",
                                amo="NO",
                                splitorder="NO",
                                split_quantity="1") 

            print ("Buy Order Response :",response)
            
            

        # Close position if there's a crossover and we already have a position
        elif shortentry and position>=0:

            # Update position variable
            position = quantity*-1
            
            # Place Smart market sell order
            response = algomojo.PlaceSmartOrder(broker=broker,
                                strategy=strategy,
                                exchange=exchange,
                                symbol=symbol,
                                action="SELL",
                                product=product,
                                pricetype="MARKET",
                                quantity=quantity,
                                price="0",
                                position_size=position,
                                trigger_price="0",
                                disclosed_quantity="0",
                                amo="NO",
                                splitorder="NO",
                                split_quantity="1") 

            print ("Sell Order Response :",response)
            
            

        # Print current position and price data
        print("Position:", position)
        print("LTP:", close[-1])
        print("Supertrend:", supertrend['Supertrend'][-2])
        print("LowerBand:", supertrend['Final Lowerband'][-2].round(2))
        print("UpperBand:", supertrend['Final Upperband'][-2].round(2))
        print("longentry:", longentry)
        print("shortentry:", shortentry)

        # Wait for 15 seconds before checking again
        time.sleep(15)

# Create and start a new thread to run the strategy
t = threading.Thread(target=supertrend_strategy)
t.start()
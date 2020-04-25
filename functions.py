""" Final Project Functions """
""" Otto Laakso """

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ochl
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

symbol = "AAPL"
interval = "1min"
api_key = "FTOFR6JUG1U8MO6Z"
plt.rcParams.update({"font.size":9})

def pullStockData(symbol, interval):
    
    ts = TimeSeries(key=api_key, output_format="pandas")
    data_ts, meta_data_ts = ts.get_intraday(symbol=symbol, interval=interval,
                                            outputsize="compact")
    
    df = data_ts
    df.reset_index(inplace=True)
    df["date"] = df["date"].map(mdates.date2num)
    
    return df

def bbands(symbol, interval):
    
    ti = TechIndicators(key=api_key, output_format="pandas")
    data_ti, meta_data_ti = ti.get_bbands(symbol=symbol, interval=interval,
                                          time_period=20, series_type="close")
    
    bbands = data_ti
    bbands.reset_index(inplace=True)
    bbands["date"] = bbands["date"].map(mdates.date2num)
    
    lower_band = bbands["Real Lower Band"]
    middle_band = bbands["Real Middle Band"]
    upper_band = bbands["Real Upper Band"]
    
    return lower_band, middle_band, upper_band

def relativeStrengthIndex(symbol, interval):
    
    ti = TechIndicators(key=api_key, output_format="pandas")
    data_ti, meta_data_ti = ti.get_rsi(symbol=symbol, interval=interval,
                                       time_period=14, series_type="close")
    
    rsi = data_ti
    rsi.reset_index(inplace=True)
    rsi["date"] = rsi["date"].map(mdates.date2num)
  
    return rsi

def graphData(symbol, interval):
    
    df = pullStockData(symbol, interval)
    
    x=0
    y=len(df["date"])
    candle_array = []
    while x < y:
        line = df["date"][x], df["1. open"][x], df["4. close"][x], df["2. high"][x], df["3. low"][x]
        candle_array.append(line)
        x+=1
    
    SP = len(df["date"][:81])
    rsi = relativeStrengthIndex(symbol, interval)
    lower_band, middle_band, upper_band = bbands(symbol, interval)
    
    #Candlestick & Bollinger Bands Graph:
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
    candlestick_ochl(ax1, candle_array[:SP], width=.0003, colorup="g", colordown="r", alpha=1.0)
    ax1.plot(df["date"][:SP], middle_band[:SP], linewidth=0.7, color="#00ffe8", alpha=.7)
    ax1.plot(df["date"][:SP], upper_band[:SP], linewidth=0.7, color="#00ffe8", alpha=.9)
    ax1.plot(df["date"][:SP], lower_band[:SP], linewidth=0.7, color="#00ffe8", alpha=.7)
    plt.fill_between(df["date"][:SP], upper_band[:SP],lower_band[:SP],facecolor="#00ffe8", alpha=0.2)
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H: %M"))    
    plt.grid(linestyle="dashed", alpha=.3)
    plt.title(symbol+" Price Action")
    plt.ylabel("Price")
    
    #Volume Graph:
    ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4)
    ax2.bar(df["date"][:SP], df["5. volume"][:SP], width=0.0003, alpha=.8)   
    ax2.fill_between(df["date"][:SP], df["5. volume"][:SP], facecolor = "#00ffe8",alpha=.4)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H: %M")) 
    ax2.axes.yaxis.set_ticklabels([])
    plt.xlabel("Time")
    plt.ylabel("Volume")

    #RSI Graph:
    ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4)
    ax0.plot(rsi["date"][-SP:], rsi["RSI"][-SP:], color="#00ffe8", alpha=.8)
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.set_ylim(20,80)
    ax0.set_yticks([30, 70])
    ax0.axhline(70, color="red", alpha=.8, linestyle="dashed")
    ax0.axhline(30, color="green", alpha=.8, linestyle="dashed")
    plt.title(symbol + " Price Action")   
    plt.ylabel("RSI")              
  
    plt.subplots_adjust(left=.09, bottom=.10, right=.94, top=.94, wspace=.20, hspace=0)
    plt.style.use("dark_background")
    plt.show()
    

df = pullStockData(symbol, interval)
graphData(symbol, interval)






    
    
    
    
    
    
    
    
    
    
    
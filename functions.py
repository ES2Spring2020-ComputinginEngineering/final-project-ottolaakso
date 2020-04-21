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

symbol = "AAPL"
interval = "1min"
api_key = "FTOFR6JUG1U8MO6Z"
plt.rcParams.update({"font.size":9})

def pullStockData(symbol, interval):
    ts = TimeSeries(key=api_key, output_format="pandas")
    data_ts, meta_data_ts = ts.get_intraday(symbol=symbol, interval=interval, outputsize="compact")
    
    df = data_ts
    df.reset_index(inplace=True)
    df["date"] = df["date"].map(mdates.date2num)
    
    return df

def movingaverage():
    
    values = df["4. close"]
    window = 20
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, "valid")
    
    return sma

def bollingerBands():
    
    sma = movingaverage()
    standard_deviation = np.std(df["4. close"])
    upperBand = sma + (standard_deviation * 2)
    lowerBand = sma - (standard_deviation * 2)
    
    return upperBand, lowerBand

def graphData(symbol, interval):
    
    df = pullStockData(symbol, interval)
    
    x=0
    y=len(df["date"])
    candle_array = []
    while x < y:
        line = df["date"][x], df["1. open"][x], df["4. close"][x], df["2. high"][x], df["3. low"][x]
        candle_array.append(line)
        x+=1
    
    sma = movingaverage()
    upperBand, lowerBand = bollingerBands()
    SP = len(df["date"][:81])
    
    ax1 = plt.subplot2grid((5,4), (0,0), rowspan=4, colspan=4)
    candlestick_ochl(ax1, candle_array, width=.0003, colorup="g", colordown="r", alpha=1.0)
    
    label_sma = "20-SMA"
    
    ax1.plot(df["date"][:SP], sma, linewidth=0.7, color="#00ffe8", label=label_sma, alpha=.7)
    ax1.plot(df["date"][:SP], upperBand[-SP:], linewidth=0.7, color="#00ffe8", alpha=.9)
    ax1.plot(df["date"][:SP], lowerBand[-SP:], linewidth=0.7, color="#00ffe8", alpha=.7)
    plt.fill_between(df["date"][:SP], upperBand[-SP:],lowerBand[-SP:],facecolor="#00ffe8", alpha=0.2)
    
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H: %M"))    
    plt.title(symbol+" Price Action")
    plt.grid(linestyle="dashed", alpha=.3)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc="upper right", fancybox=True)
    
    ax2 = plt.subplot2grid((5,4 ), (4,0), sharex=ax1, rowspan=1, colspan=4)
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax2.bar(df["date"], df["5. volume"], width=0.0003   )
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H: %M"))    
    ax2.axes.yaxis.set_ticklabels([])
    plt.fill_between(df["date"], df["5. volume"], facecolor = "#00ffe8", alpha=0.35)
    plt.ylabel("Volume")
    plt.xlabel("Time")
    
    plt.subplots_adjust(left=.09, bottom=.10, right=.94, top=.94, wspace=.20, hspace=0)
    plt.style.use("dark_background")
    plt.show()
    

df = pullStockData(symbol, interval)
graphData(symbol, interval)

    
    
    
    
    
    
    
    
    
    
    
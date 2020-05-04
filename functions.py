""" Final Project Functions """
""" Otto Laakso """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.animation as animation
from mpl_finance import candlestick_ochl
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

symbol = "IBM"
interval = "1min"
api_key = "FTOFR6JUG1U8MO6Z"

fig = plt.figure()

def pullStockData(symbol, interval):
# Parameters: stock symbol and time interval
# Creates a data frame with open, high, low, close, and date data points
# Returns the data frame
    
    ts = TimeSeries(key=api_key, output_format="pandas")
    data_ts, meta_data_ts = ts.get_intraday(symbol=symbol, interval=interval,
                                            outputsize="compact")
    
    df = data_ts
    df.reset_index(inplace=True)
    df["date"] = df["date"].map(mdates.date2num)
    
    return df

def bbands(symbol, interval):
# Parameters: stock symbol and time interval
# Calculates three Bollinger Bands for the given stock
# Returns the lower, upper, middle band, and standard deviation data points
    
    ti = TechIndicators(key=api_key, output_format="pandas")
    data_ti, meta_data_ti = ti.get_bbands(symbol=symbol, interval=interval,
                                          time_period=20, series_type="close")
    
    bbands = data_ti
    bbands.reset_index(inplace=True)
    bbands["date"] = bbands["date"].map(mdates.date2num)
    
    lower_band = bbands["Real Lower Band"]
    middle_band = bbands["Real Middle Band"]
    upper_band = bbands["Real Upper Band"]
    sd = middle_band - lower_band
    
    return lower_band, middle_band, upper_band, sd

def relativeStrengthIndex(symbol, interval):
# Parameters: stock symbol and time interval
# Calculates the relative strength index for the given stock
# Returns a data frame with RSI and time values
    
    ti = TechIndicators(key=api_key, output_format="pandas")
    data_ti, meta_data_ti = ti.get_rsi(symbol=symbol, interval=interval,
                                       time_period=14, series_type="close")
    
    rsi = data_ti
    rsi.reset_index(inplace=True)
    rsi["date"] = rsi["date"].map(mdates.date2num)
    
    return rsi

def candleArray(df):
# Parameters: data frame with open, high, low, close, and date
# Rearranges the data points into an array suitable for candlestick charting
# Returns the candlestick array
    
    x=0
    y=len(df["date"])
    candle_list = []
    while x < y:
        line = df["date"][x], df["1. open"][x], df["4. close"][x], df["2. high"][x], df["3. low"][x]
        candle_list.append(line)
        x+=1
    
    candle_array = np.array(candle_list)
    
    return candle_array

def tradingAlgorithm(candle_array, upper_band, lower_band, sd, rsi, SP, ax, df):
# Parameters: array of candlesticks, upper and lower bollinger bands, RSI values, starting point, and axis
# Ffor each data point, tests whether a buy or sell signal is created and graphs them with the stop loss level
# Returns None
    
    rs = len(rsi)
    close_prices = candle_array[:,2]
    
    for i in range(len(candle_array[:SP])):
        
        if close_prices[i] < lower_band[:SP][i] and rsi["RSI"][-SP:][rs-i] < 30:
            ax.axvline(df["date"][:SP][i], color="lime", label="Buy",
                       linestyle="dashed", alpha=1.0)
            ax.axhline(close_prices[i]-sd[i], color="red", label="Stop Loss",
                       linestyle="dashed", alpha=.8)
            ax.legend()
            break
        
        elif close_prices[i] > upper_band[:SP][i] and rsi["RSI"][rs-i] > 70:
             ax.axvline(df["date"][:SP][i], color="red", label="Sell",
                        linestyle="dashed", alpha=1.0)
             ax.axhline(close_prices[i]+sd[i], color="red", label="Stop Loss",
                       linestyle="dashed", alpha=.8)
             ax.legend()
             break
    return

def graphData(symbol, interval):
# Parameters: stock symbol and time interval
# Graphs the candlestick chart, volume, RSI, and bollinger bands
# Graphs "Sell" and "Buy" signals given by the trading algorithm every 60 seconds
# Returns None
    while True:     
        fig.clf()
        SP = 81
        df = pullStockData(symbol, interval)
        candle_array = candleArray(df)
        rsi = relativeStrengthIndex(symbol, interval)
        lower_band, middle_band, upper_band, sd = bbands(symbol, interval)
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
        # Trading Algorithm
        ax = ax1
        tradingAlgorithm(candle_array, upper_band, lower_band, sd, rsi, SP, ax, df)
        plt.subplots_adjust(left=.09, bottom=.10, right=.94, top=.94, wspace=.20, hspace=0)
        plt.style.use("dark_background")
        plt.draw()
        plt.pause(60)
        
graphData(symbol, interval)
    
    
    
    
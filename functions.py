""" Final Project Functions """
""" Otto Laakso """

from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import mplfinance
import matplotlib.dates as mdates

plt.rcParams.update({"font.size":9})
api_key = "FTOFR6JUG1U8MO6Z"
symbol = "TSLA"
interval = "1min"

def pullStockData(symbol, interval):
    ts = TimeSeries(key=api_key, output_format="pandas")
    data_ts, meta_data_ts = ts.get_intraday(symbol=symbol, interval=interval, outputsize="compact")
    
    df = data_ts
    print(df)
    print(df["1. open"][0])

    return df

def graphData(symbol, interval):
    
    df = pullStockData(symbol, interval)
    
    #candelstick(ax1, dochl, width=13fasdfas)

    fig = plt.figure()
    ax1 = plt.subplot2grid((5,4), (0,0), rowspan=4, colspan=4)
    ax1.plot(df["1. open"])
    ax1.plot(df["2. high"])
    ax1.plot(df["3. low"])
    ax1.plot(df["4. close"])
    ax1.grid(alpha=.4, linestyle="dashed")
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H: %M"))    
    plt.title(symbol+" Price Action")
    plt.xlabel("Date")
    plt.ylabel("Price")
    
    ax2 = plt.subplot2grid((5,4 ), (4,0), sharex=ax1, rowspan=1, colspan=4)
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H: %M"))    
    ax2.plot(df["5. volume"])
    ax2.axes.yaxis.set_ticklabels([])
    plt.ylabel("Volume")
    plt.xlabel("Time")
    
    #plt.setp(ax1.get_xsticklabels(), visible=False)
    plt.subplots_adjust(left=.09, bottom=.18, right=1, top=.94, wspace=.20, hspace=0)
    plt.style.use("dark_background")
    plt.show()
    

pullStockData(symbol, interval)
graphData(symbol, interval)

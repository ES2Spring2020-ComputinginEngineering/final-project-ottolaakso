""" Final Project Functions """
""" Otto Laakso """

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import matplotlib.animation as animation

api_key = "FTOFR6JUG1U8MO6Z"
symbol = "AAPL"
interval = "1min"

def stockData(symbol, interval):
    ts = TimeSeries(key=api_key, output_format="pandas")
    data_ts, meta_data_ts = ts.get_intraday(symbol=symbol, interval=interval, outputsize="compact")
    
    data_frame = data_ts["4. close"]
    print(data_frame)

    return data_frame


stockData(symbol, interval)

""" Final Project Driver """
""" Otto Laakso """

import functions as fns
import matplotlib.pyplot as plt

symbol = "XOM"
interval = "1min"
api_key = "FTOFR6JUG1U8MO6Z"

fig = plt.figure()

df = fns.pullStockData(symbol, interval)

fns.liveData(symbol, interval, fig)
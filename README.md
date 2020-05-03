Otto Laakso
ES2 Final Project

# Coding an Algorithmic Trading Bot

The goal of this project was to design an algorithm that generates "Buy" and "Sell" commands for the user based on the historical price action of the given stock.

## Instructions

1. Open the file "main.py"
2. Enter the stock symbol (i.e. symbol="AAPL") and time interval (i.e. interval="1min")
3. Click on the Spyder menu "python" --> "Preferences" --> "IPython console"
4. In the IPython console, click "Graphics" and change "Graphics Backend" to "Qt5"
5. Press OK and run the program twice, closing the pop up window in between the runs.
6. If the API call frequency is exceeded, wait one minute and run the program again 
7. Use the interactive toolbar on the pup up window to navigate the graph

## File List

- functions.py : Contains all functions needed for the algorithm
- main.py : Driver file for the algorithmic trading bot, run according to instructions.
- README.md : File containing helpful information regarding the program

## Features

The algorithm:
- Uses Alpha Vantage for market data
- Uses Pandas data frames for data processing
- Uses matplotlib for graphing

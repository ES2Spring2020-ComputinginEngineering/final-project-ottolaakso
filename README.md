Otto Laakso
ES2 Final Project

# Coding an Algorithmic Trading Bot

The goal of this project was to design an algorithm that generates "Buy" and "Sell" commands for the user based on the historical price action of the given stock.

## Instructions

1. Open the file "main.py"
2. Enter the stock symbol and time interval (i.e. interval="1min"). The symbol "XOM" is recommended since Alpha Vantage doesn't provide live data for some other stocks.
3. Click on the Spyder menu "python" --> "Preferences" --> "IPython console"
4. In the IPython console, click "Graphics" and change "Graphics Backend" to "Qt5"
5. Press OK and run the program
6. It usually takes one or two data updates for the visual layout to function properly. For the first two updates, close the pop up window and wait for it to re-appear until the new pop up window displays all graphs and axes correctly.
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

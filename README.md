# crypto_trading
Project for trading cryptocurrency pairs through Robinhood using the robin_stocks python API and the talib python API.  It currently decides on positions using the Moving Average Convergence Divergence (MACD) technical indicator (https://www.investopedia.com/trading/macd/), deciding to hold a specific position if the MACD line is both above 0 and above the MACD trigger line and exiting a position if the MACD line either drops below 0 or below the MACD trigger line.

main.py is where the magic happens; this controls your Robinhood account and actually places orders based on the methods described above.

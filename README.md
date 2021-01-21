# crypto_trading
Project for trading cryptocurrency pairs through Robinhood using the robin_stocks python API and the talib python API.  It currently decides on positions using the Moving Average Convergence Divergence (MACD) technical indicator (https://www.investopedia.com/trading/macd/), deciding to hold a specific position if the MACD line is both above 0 and above the MACD trigger line and exiting a position if the MACD line either drops below 0 or below the MACD trigger line.  You will need a Robinhood account for this to work.

main.py is where the magic happens; this controls your Robinhood account and actually places orders based on the methods described above.  crypto_info.csv is made to simply store the last $ amount of each crypto that you held when you sell.  So, if you're holding $100 worth of BTC and it gets sold, then $100 will be saved into crypto_info.csv and then whenever the algorithm decides to enter back into the position, it will enter with the same amount of $.

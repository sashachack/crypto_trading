import robin_stocks as r
import talib as tl
import pandas as pd
import time
import datetime as dt

username = 'your_username'
password = 'your_password'
r.login(username, password)

info = pd.read_csv(r'crypto_info.csv')


def get_open_positions():
    crypto_positions = r.crypto.get_crypto_positions()
    positions = {}
    for cp in crypto_positions:
        sym = cp['currency']['code']
        quant = cp['quantity']
        if float(quant) > 0.001:
            positions[sym] = quant
    return positions


def macd_search(syms):
    data = {}
    macd, macd_signal, macd_hist = {}, {}, {}

    for sym in syms:
        data[sym] = pd.DataFrame(r.crypto.get_crypto_historicals(sym, interval='day',
                                                                 span='3month')).loc[:, 'close_price'].tolist()
        data[sym].append(r.crypto.get_crypto_quote(sym)['bid_price'])  # cuz it doesn't include current
        data[sym] = pd.Series(data[sym])

    for sym in syms:
        macd[sym], macd_signal[sym], macd_hist[sym] = tl.MACD(data[sym])

    # Now we'll determine the move for each, with 0 being nothing, 1 being bull, -1 being bear
    crypto_moves = {}

    for sym in syms:
        macd_val = macd[sym].values[-1]
        signal_val = macd_signal[sym].values[-1]
        if macd_val > 0 and macd_val > signal_val:  # bullish
            crypto_moves[sym] = 1
        elif macd_val < 0 and macd_val < signal_val:  # bearish
            crypto_moves[sym] = -1
        else:
            crypto_moves[sym] = 0

    return crypto_moves


def trade(all_coins, positions, moves):
    info = pd.read_csv(r'crypto_info.csv')
    for sym in all_coins:
        move = moves[sym]
        quant = float(positions[sym]) if sym in positions else 0
        worth = float(r.crypto.get_crypto_quote(sym)['mark_price']) * quant
        if move == 1:  # wanna be in this pos
            if sym in positions:  # already in this pos
                continue
            else:  # time to buy into the pos
                old_worth = round(float(info.at[0, sym]), 2)
                print('Let\'s buy {} worth of {}'.format(old_worth, sym))
                # buy old_worth amt
                r.orders.order_buy_crypto_by_price(sym, old_worth)
                info.at[0, sym] = 0
        else:  # don't wanna be in this pos
            if sym not in positions:  # not in this pos
                continue
            else:  # time to get out of this pos
                print('Let\'s sell {:.4f} {}'.format(quant, sym))
                r.orders.order_sell_crypto_by_quantity(sym, round(quant, 8))
                info.at[0, sym] = round(worth, 2)
                # sell all of it
    info.to_csv(r'crypto_info.csv', index=False)


while 2 == 2:
    all_pos = list(info.columns)
    open_pos = get_open_positions()
    movements = macd_search(all_pos)
    trade(all_pos, open_pos, movements)
    time.sleep(60)

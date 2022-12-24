import talib, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# COMMISSION = 0.001
LIQ_MEMORY = 120
DEPTH = 5
# in_position = "null"

# budget = 1000
# coin_amount = 0

df = pd.read_csv("BTC-2021min-reversed.csv", index_col=2, parse_dates=True)

liquidities = []
counter = 0
liqCandle = []
dusuyor = False
liqAlindi = False

for x in range(0, len(df), 1):
    tdf = df[x-LIQ_MEMORY:x]
    tdf.index.name = 'date'

    candle = df[x:x+1]
    prev_candle = df[x+1:x+2]

    lowVal = float(candle['low'])
    prevLowVal = float(prev_candle['low'])
    print(candle.to_numpy()[0][5], " ", counter)
    if len(liqCandle) == 0:
        liqCandle = candle.to_numpy()

    if lowVal < prevLowVal:
        dusuyor = True
        if lowVal <= liqCandle[0][5]:
            counter = 0
            liqCandle = candle.to_numpy()
        elif lowVal > liqCandle[0][5]:
            counter += 1

        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    elif prevLowVal <= lowVal:
        dusuyor = False
        if counter == 0:
            liqCandle = prev_candle.to_numpy()
            # print(liqCandle,"len(liqCandle): ",len(liqCandle), "   ", liqCandle[0][5])
        counter += 1
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    if counter == DEPTH:
        liquidities[-DEPTH] = df.iloc[x - DEPTH]['low'] - 5
        # print(df.iloc[x-DEPTH])
        counter = 0
        liqCandle = candle.to_numpy()

    if len(liquidities) == len(tdf) and len(liquidities) == LIQ_MEMORY and x % 10 == 0:
        buy_markers = mpf.make_addplot(liquidities, type='scatter', markersize=60, marker='^')
        try:
            mpf.plot(tdf, figratio=(42,24), type='candle', tight_layout=True, datetime_format='%b %d, %H:%M', addplot=buy_markers)
        except ValueError:
            print(ValueError)
            pass

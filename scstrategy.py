import talib, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# COMMISSION = 0.001
LIQ_MEMORY = 100
DEPTH = 5
# in_position = "null"

# budget = 1000
# coin_amount = 0

df = pd.read_csv("BTC-2021min-reversed.csv", index_col=2, parse_dates=True)

liquidities = []
counter = 0
liqCandle = []
dusuyor = False

for x in range(0, len(df), 1):
    tdf = df[x-LIQ_MEMORY:x]
    tdf.index.name = 'date'

    candle = df[x:x+1]
    prev_candle = df[x+1:x+2]

    lowVal = float(candle['low'])
    prevLowVal = float(prev_candle['low'])

    if lowVal < prevLowVal:
        dusuyor = True
        if len(liqCandle) != 0:
            if lowVal < liqCandle[0][5]:
                counter = 0
                liqCandle = []
        if len(liqCandle) != 0:
            if lowVal > liqCandle[0][5]:
                counter += 1
        if len(liqCandle) == 0:
            counter = 0

        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    elif prevLowVal < lowVal:
        dusuyor = False
        if counter == 0:
            liqCandle = prev_candle.to_numpy()
            print(liqCandle,"len(liqCandle): ",len(liqCandle), "   ", liqCandle[0][5])
        counter += 1
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    if counter == DEPTH:
        liquidities[-DEPTH+1] = df.iloc[x - DEPTH +1]['low'] - 10
        print(df.iloc[x-DEPTH])
        counter = 0
        liqCandle = []

    if len(liquidities) == len(tdf) and len(liquidities) == LIQ_MEMORY and x%(LIQ_MEMORY/2) ==0:
        buy_markers = mpf.make_addplot(liquidities, type='scatter', markersize=60, marker='^')
        try:
            mpf.plot(tdf, type='candle', tight_layout=True, datetime_format='%b %d, %H:%M', addplot=buy_markers)
        except ValueError:
            print(ValueError)
            pass
    print(len(liquidities), liquidities, lowVal, dusuyor, counter)

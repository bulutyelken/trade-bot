import talib, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

COMMISSION = 0.001
LIQ_MEMORY = 100

in_position = "null"

budget = 1000
coin_amount = 0

df = pd.read_csv("BTC-2021min-reversed.csv", index_col=2, parse_dates=True)



liquidities = []
counter = 0

mins = 0
hours = 0.0
days = 0.0
liqLevel = 0.0


for x in range(10, len(df), 1):
    tdf = df[x:x+100]
    tdf.index.name = 'date'

    candle = df[x:x+1]
    prev_candle = df[x+1:x+2]
    mins += 1
    lowVal = float(candle['low'])
    prevLowVal = float(prev_candle['low'])
    if lowVal < prevLowVal:
        counter = 0
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    elif prevLowVal < lowVal:
        if counter == 1:
            liqLevel = lowVal
        counter += 1
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    if counter == 5:
        liquidities.append(liqLevel)
        # liquidities.append(tdf.iloc[x]['low'])
        print(liquidities)
        counter = 0
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)
        hours = mins / 60
        days = hours / 24
        buy_markers = mpf.make_addplot(liquidities, type='scatter', markersize=120, marker='^')
        apds = [buy_markers]
        if len(liquidities) == len(tdf):
            mpf.plot(tdf, type='candle', tight_layout=True, datetime_format='%b %d, %H:%M', addplot=apds)

    print(len(liquidities))
import talib, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# COMMISSION = 0.001
LIQ_MEMORY = 60
# in_position = "null"

# budget = 1000
# coin_amount = 0

df = pd.read_csv("BTC-2021min-reversed.csv", index_col=2, parse_dates=True)

liquidities = []
counter = 0

liqCandle = []
dusuyor = False
for x in range(10, len(df), 1):

    tdf = df[x:x+LIQ_MEMORY]
    tdf.index.name = 'date'

    candle = df[x:x+1]
    prev_candle = df[x+1:x+2]

    lowVal = float(candle['low'])
    prevLowVal = float(prev_candle['low'])

    if lowVal < prevLowVal:
        # if lowVal < float(liqCandle.values[5]):  -- ...onun yerine buradaki gibi prevCandle yerine liqCandle'a bakmamiz lazim!
        #     counter = 0  -- SORUN BURADA MUHTEMELEN, candle bir önceki candledan düsükse direkt counter'i 0'lıyor. bunun fixlenmesi lazim...
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)
        dusuyor = True
    elif prevLowVal < lowVal:
        if counter == 1:
            liqCandle = candle
        dusuyor = False
        counter += 1
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    if counter == 3:
        for y in range(5):
            liquidities.pop(-1)

        liquidities.append(df.iloc[x-4]['low']-20)
        # liquidities.append(tdf.iloc[x]['low'])
        print(liquidities)
        counter = 0
        liqCandle = []
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    if len(liquidities) == len(tdf) and len(liquidities) == LIQ_MEMORY and x % LIQ_MEMORY == 0:
        buy_markers = mpf.make_addplot(liquidities, type='scatter', markersize=60, marker='^')
        apds = [buy_markers]
        try:
            mpf.plot(tdf, type='candle', tight_layout=True, datetime_format='%b %d, %H:%M', addplot=buy_markers)
        except ValueError:
            pass

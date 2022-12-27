import talib, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# COMMISSION = 0.001
LIQ_MEMORY = 100
DEPTH = 6
# in_position = "null"
# budget = 1000
# coin_amount = 0

df = pd.read_csv("BTC-2021min-reversed.csv", index_col=2, parse_dates=True).iloc[90000:]

liquidities = []
liqCandle = []
counter = 0
dususMumlari = [np.nan]

for x in range(0, len(df), 1):
    tdf = df[x - LIQ_MEMORY:x]
    tdf.index.name = 'date'

    candle = df[x:x + 1]
    prev_candle = df[x + 1:x + 2]

    lowVal = float(candle['low'])
    prevLowVal = float(prev_candle['low'])

    if len(liqCandle) == 0:
        liqCandle = candle.to_numpy()

    if lowVal < prevLowVal:
        if lowVal <= liqCandle[0][5]:
            counter = 0
            liqCandle = candle.to_numpy()
        elif lowVal > liqCandle[0][5]:
            counter += 1
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    elif prevLowVal <= lowVal:
        if counter == 0:
            liqCandle = prev_candle.to_numpy()
            # print(liqCandle,"len(liqCandle): ",len(liqCandle), "   ", liqCandle[0][5])
        counter += 1
        liquidities.append(np.nan)
        if len(liquidities) > LIQ_MEMORY:
            liquidities.pop(0)

    for i in range(len(liquidities) - 1):
        if len(liquidities) >= LIQ_MEMORY:
            if liquidities[i] > float(candle['low']):
                liquidities[i] = np.nan


    if counter == DEPTH:

        liquidities[-DEPTH] = df.iloc[x - DEPTH]['low'] - 5

        # print(df.iloc[x-DEPTH])
        counter = 0
        liqCandle = candle.to_numpy()

    # if float(candle['open']) > float(candle['close']):
    #     dususMumlari.append(float(candle['low']))
    # elif float(candle['open']) <= float(candle['close']):
    #     dususMumlari.append(np.nan)
    # if len(dususMumlari) > LIQ_MEMORY:
    #     dususMumlari.pop(0)

    # ------------------------------------------------------------------------------------------,

    if len(liquidities) == len(tdf) and len(liquidities) == LIQ_MEMORY:
        buy_markers = mpf.make_addplot(liquidities, type='scatter', markersize=30, marker='^', color='r')
        try:
            mpf.plot(tdf, figratio=(16, 9), figscale=1.2, type='candle', tight_layout=True, datetime_format='%b %d, %H:%M', addplot=buy_markers)
        except ValueError as e:
            print(e)
            pass
    # print(float(candle['open']), "-", float(candle['close']), " =  ", float(candle['open']) - float(candle['close']))

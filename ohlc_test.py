import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import mplfinance as mpf
import csv
def percentB_belowzero(low,price):
    import numpy as np
    signal = []
    previous = -1.0
    for date, value in low.items():
        if value < 0 and previous >= 0:
            signal.append(price[date]*0.99)
        else:
            signal.append(np.nan)
        previous = value
    return signal


df = pd.read_csv('BTC-2021min-reversed.csv', index_col=2, parse_dates=True)

tdf = df.loc['2022-02-19 12:16:00':'2022-02-19 16:43:00', :]

tdf.index.name = 'date'
signal = percentB_belowzero(tdf['low'], tdf['close'])
apd = mpf.make_addplot(signal, type='scatter')



# apd = mpf.make_addplot(tdf['low']-20, type='scatter')


mpf.plot(tdf, type='candle', tight_layout=True,datetime_format='%b %d, %H:%M')
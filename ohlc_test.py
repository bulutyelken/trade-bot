import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import mplfinance as mpf
import csv

df = pd.read_csv('BTC-2021min-reversed.csv',index_col=2,parse_dates=True,nrows=1000)

# tdf = df.loc['2022-02-19 00:16:00':'2022-03-01 03:43:00', :]

df.index.name = 'date'
df.shape
df.head(3)
df.tail(3)
apd = mpf.make_addplot(df['low']-20,type='scatter')




mpf.plot(df,addplot=apd,type='candle',tight_layout=True,datetime_format='%b %d, %H:%M')
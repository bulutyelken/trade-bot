import talib, numpy
import pandas as pd

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
COMMISSION = 0.001

closes = []
indexLine = 0
in_position = "null"

budget = 1000
coin_amount = 0

df = pd.read_csv("BTC-2021min.csv")


for x in range(len(df) - 1, 1, -1):
    indexLine = indexLine + 1
    csv_line = df[x:x+1]
    closeVal = float(csv_line['close'])
    closes.append(closeVal)

    if indexLine > 20:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes,RSI_PERIOD)
        last_rsi = rsi[-1]



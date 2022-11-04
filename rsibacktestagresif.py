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

    if indexLine > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes,RSI_PERIOD)
        last_rsi = rsi[-1]

        if last_rsi < RSI_OVERSOLD:
            if in_position == "null":
                print("Oversold. Entered long position.",closeVal)
                budget = budget - budget * COMMISSION
                coin_amount = budget / closeVal
                budget = 0
                in_position = "long"
            if in_position == "short":
                print("Oversold. Closed short position.")
                budget = -coin_amount * closeVal
                coin_amount = 0
                in_position = "null"
                print("Budget = ", budget)
                print("------------------------------------------------------------")

        if last_rsi > RSI_OVERBOUGHT:
            if in_position == "long":
                print("Overbought. Closed Long position.",closeVal)
                coin_amount = coin_amount - coin_amount * COMMISSION
                budget = coin_amount * closeVal
                coin_amount = 0
                print("Budget = ", budget)
                print("------------------------------------------------------------")
                in_position = "null"
            if in_position == "null":
                print("Overbought. Entered short position.", closeVal)
                budget = budget - budget * COMMISSION
                coin_amount = -budget / closeVal
                budget = 0
                in_position = "short"

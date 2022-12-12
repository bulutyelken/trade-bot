import talib, numpy
import pandas as pd
import matplotlib.pyplot as plt


COMMISSION = 0.001

in_position = "null"

budget = 1000
coin_amount = 0

df = pd.read_csv("BTC-2021min.csv")

liquidities = []
counter = 0
mins = 0
hours = 0.0
days = 0.0
liqLevel = 0.0
moment = []
price = []
# x=[1,2,3,4,5,6,7,8]
# y=[0.1,0.2,0.5,0.6,0.8,0.8,0.9,1.3]
# plt.plot(x,y)
# plt.show()
plt.xlabel("Time")
plt.ylabel("Price")
plt.title("Price and Swing Lows")

for x in range(len(df) - 10, 1, -1):
    candle = df[x:x+1]
    prev_candle = df[x+1:x+2]
    mins += 1
    lowVal = float(candle['low'])
    prevLowVal = float(prev_candle['low'])

    price.append(float(candle['close']))
    if len(price) == 61:
        price.pop(0)

    if len(price) == len(moment) and len(moment) == 60:
        plt.plot(moment, price, c='red')
        if len(liquidities) == 60:
            plt.show()

    if lowVal < prevLowVal:
        liquidities.append(float(candle['close']))
        counter = 0

    elif prevLowVal < lowVal:
        if counter == 1:
            liqLevel = lowVal
        counter += 1

    if counter == 5:
        liquidities.append(liqLevel)
        counter = 0
        if len(liquidities) > 60:
            liquidities.pop(0)
        hours = mins / 60
        days = hours / 24
        print("liqs: ", len(liquidities), "  moment: ", len(moment))
        print("")
        print(len(price))
        print("")
        if len(moment) == len(liquidities) and len(liquidities) == 60:
            plt.plot(moment, liquidities, c='blue', marker='o')

    mom = str(candle['date'])
    moment.append(mom[20:29])
    if len(moment) == 61:
        moment.pop(0)





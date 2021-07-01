import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
from datetime import timedelta
yf.pdr_override()

stock=input("Enter a stock ticker : ")
ma = input("Enter the two moving average lines : ")
ma1,ma2 = ma.split(',')
edate = dt.datetime.now()
sdate = edate - dt.timedelta(days=365)
df = pdr.get_data_yahoo(stock,sdate,edate)

df['{} SMA'.format(ma1)] = df.iloc[:,4].rolling(window=int(ma1)).mean()
df['{} SMA'.format(ma2)] = df.iloc[:,4].rolling(window=int(ma2)).mean()

capital=100000
pos=0
num=0
print(df)
for i in df.index:
    num = num+1
    if df["{} SMA".format(ma1)][i]>df["{} SMA".format(ma2)][i] and pos==0:
        pos=1
        buy_price=df["Adj Close"][i]
        qty = int(capital/buy_price)
        capital = capital - qty*buy_price
        print("Bought {} shares at {}".format(qty,buy_price))
    elif (df["{} SMA".format(ma1)][i]<df["{} SMA".format(ma2)][i]) and pos==1:
        pos=0
        sell_price=df["Adj Close"][i]
        capital = capital + sell_price*qty
        print("Sold {} shares at {}".format(qty,sell_price))
    elif df['Adj Close'].count()==num and pos==1:
        pos=0
        sell_price = df["Adj Close"][i]
        capital = capital + sell_price*qty
        print("Sold {} shares at {}".format(qty,sell_price))

print("Total Capital is {}".format(capital))

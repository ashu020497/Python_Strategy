'''
    Strategy accounts for three conditions :
    1. Buy is triggered when close is less than 7 day low and greater than 200 SMA
    2. Sell is triggered when close is greater than 7 day high
    3. SL is triggered after 2*ATR(20)
'''
import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
import matplotlib.pyplot as plt

yf.pdr_override()

stock="^DJI"
edate = dt.datetime.now()
sdate = edate-dt.timedelta(days=365)
df = pdr.get_data_yahoo(stock,sdate,edate)

# Creates 7 day high and 7 day low column
df['7_day_high'] = df.iloc[:,1].rolling(7).max().shift()
df['7_day_low'] = df.iloc[:,2].rolling(7).min().shift()

# Create ATR column in dataframe
high_low = df['High']-df['Low']
high_close = np.abs(df['High']-df['Close'].shift())
low_close = np.abs(df['Low']-df['Close'].shift())
df_closes = pd.concat([high_low,high_close,low_close], axis=1)   # Creating another df frame with the three possible value of True Range
true_range = np.max(df_closes,axis=1)
df["ATR"] = true_range.rolling(20).mean()

# Compute the value of 200 SMA
df["200 SMA"]=df["Close"].rolling(200).mean()

# Condition for buying and selling
pos=0
capital = 100000
count=0
trade=0
duration = 0
for i in df.index:
    count +=1
    if df['Close'][i] <= df['7_day_low'][i] and df['Close'][i] > df['200 SMA'][i] and pos==0:
        pos=1
        buy_price = df['Close'][i]
        qty = int(capital/buy_price)
        capital -= qty*buy_price
        trade+=1
        duration_start = i
        print("Buy is triggered at {} on {}".format(buy_price,i.strftime("%d-%m-%Y")))
    elif df['Close'][i] >= df['7_day_high'][i] and pos == 1:
        pos=0
        sell_price = df['Close'][i]
        capital += qty*sell_price
        duration += (i-duration_start).days
        print("Sell is triggered at {}".format(sell_price))
    elif (pos==1 and (buy_price-df['Close'][i])>2*df['ATR'][i]) or (df['Close'].count() == count):
        pos=0
        sell_price = df['Close'][i]
        capital += qty*sell_price
        duration += (i-duration_start).days
        print("Sell is triggered at {}".format(sell_price))

total_return = ((capital-100000)/100000)*100
print("Final Capital is {} and total return is {} after a period of {}".format(capital,total_return,duration))
print("Total Number of trades taken is {}".format(count))

#print(df)


'''writer =pd.ExcelWriter('7output.xlsx')
df.to_excel(writer)
writer.save()
'''

import numpy as np
import pandas as pd
import datetime as dt
from smartapi import SmartConnect
from tkinter import *
from tkinter.filedialog import askopenfilename

obj = SmartConnect(api_key='qAHQRDyJ ')
data = obj.generateSession('A545511','Kite@666')

root = Tk()
filePath = askopenfilename()
root.withdraw()

list = pd.read_excel(filePath)

for i in list.index:
    share = str(list['Symbol'][i])
    share_token = str(list['Token'][i])
    df = pd.DataFrame(columns={'Date','Close'})
    param = {'exchange':'NSE','symboltoken':share_token,'interval':'ONE_DAY','fromdate':'2020-07-08 09:15','todate':'2021-07-13 03:30'}
    stock_candle = obj.getCandleData(param)
    for x in stock_candle['data']:
        date,time = x[0].split('T')
        df = df.append({'Date':date,'Close':x[4]},ignore_index=True)
        df['200SMA'] = df['Close'].rolling(200).mean()
    latest_close = float(df.iloc[-1,0])
    latest_SMA = float(df.iloc[-1,2])
    if (latest_SMA*0.98) < latest_close < (latest_SMA*1.02):
        print(share, ' near 200 Day SMA')

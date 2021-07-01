import pandas as pd
from smartapi import SmartConnect
import os
from pandas import ExcelWriter
import datetime as dt
import ta
from tkinter.filedialog import askopenfilename

obj = SmartConnect(api_key='ed56YlmG ')
session = obj.generateSession('A545511','Kite@666')

param = {'exchange':'NSE','symboltoken':'4963','interval':'FIFTEEN_MINUTE','fromdate':'2021-01-01 09:15','todate':'2021-06-22 15:30'}

filepath = askopenfilename(initialdir = 'C://Users//ashu0//Desktop')
df = pd.read_excel(filepath)
df1 = pd.DataFrame()
for i in df.index:
    x,y = df['symbol'][i].split('-')
    if y=='EQ':
        df1.append(df[i],ignore_index=True)
print(df.head())

import numpy as np
import pandas as pd
import datetime as dt
from smartapi import SmartConnect
from pandas import ExcelWriter
from tkinter import *
from tkinter.filedialog import askopenfilename

# Generate Angel Broking Session
obj = SmartConnect(api_key='nsfiZ9Mj')
data = obj.generateSession('A545511','Kite@666')

# Getting location of nifty 500 list
root = Tk()
filePath = askopenfilename()
root.withdraw()
nifty_500 = pd.read_excel(filePath)

df = pd.DataFrame(columns=['Time','Open','High','Low','Close','Volume'])

for i in nifty_500.index:
    param = {'exchange':'NSE','symboltoken':str(nifty_500['Token'][i]),'interval':'ONE_DAY','fromdate':'2020-01-01 09:15','todate':'2021-06-22 15:30'}
    info = obj.getCandleData(param)
    for i in info['data']:
        x,y = i[0].split('T')
        df = df.append({'Time': x,'Open':i[1],'High':i[2],'Low':i[3],'Close':i[4],'Volume':i[5]},ignore_index=True)

    year_high = df['High'].max()
    if (df.iloc[4,-1] > (0.96 * year_high) ) and ( df.iloc[4,-1] < (1.04 * year_high) ):
        print(nifty_500['Symbol'][i])

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pandas import ExcelWriter

yf.pdr_override()

filePath = askopenfilename(initialdir = "C://Users//ashu0//Desktop//Python")
stocklist=pd.read_excel(filePath)
edate = dt.datetime.now()
sdate = edate - dt.timedelta(days=180)
volume_list = pd.DataFrame(columns=['Index','Stock'])
for i in stocklist.index:
    stock = stocklist["Symbol"][i]+".NS"
    df = pdr.get_data_yahoo(stock,sdate,edate)
    avg_vol = df.iloc[:,5].mean()
    count=0

    #print("The Average Volume for {} is {}".format(stocklist["Symbol"][i],avg_vol))
    if df.iloc[-1,5]>1.2*avg_vol:
        count = count+1
        print("There is a volume breakout in {}".format(stocklist["Company Name"][i]))
        volume_list.append({'Index':count,'Stock':stocklist['Symbol'][i]},ignore_index=True)
        writer=ExcelWriter('volume_output.xlsx')
        volume_list.to_excel(writer,"Sheet 1")
        writer.save()
print(volume_list)

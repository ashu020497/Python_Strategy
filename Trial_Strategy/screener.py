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

#root=Tk()
filePath = askopenfilename(initialdir = "C://Users//ashu//Desktop", title="Choose Excel File")
stocklist=pd.read_excel(filePath)
startdate = dt.datetime(2020,1,1)
enddate = dt.datetime.now()

total_return_list = pd.DataFrame(columns=['Stock','Base Capital','Final Capital','Total Return'])
emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
for i in stocklist["Symbol"]:
    stock=i+str(".NS")
    df = pdr.get_data_yahoo(stock,startdate,enddate)
    pos=0
    capital=50000
    num=0
    for x in emasUsed:
        ema=x
        df["{} EMA".format(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)
    for y in df.index:
        cmin=min(df["3 EMA"][y],df["5 EMA"][y],df["8 EMA"][y],df["10 EMA"][y],df["12 EMA"][y],df["15 EMA"][y])
        cmax=max(df["30 EMA"][y],df["35 EMA"][y],df["40 EMA"][y],df["45 EMA"][y],df["50 EMA"][y],df["60 EMA"][y])
        num+=1
        close = df["Adj Close"][y]
        if(cmin>cmax and pos==0):
             pos=1
             bp=close
             qty = int(capital/bp)
             capital -= bp*qty
        elif(cmin<cmax and pos==1):
            pos=0
            sp=close
            capital += sp*qty
        if(num==df["Adj Close"].count() and pos==1):
            pos=0
            sp=close
            capital += sp*qty


    treturn = ((capital-50000)/50000)*100
    #print("Total Return for {} is {}%".format(i,treturn))
    total_return_list = total_return_list.append({'Stock': i,'Base Capital': 50000, 'Final Capital': capital, 'Total Return': treturn},ignore_index=True)
#print(total_return_list)

newFile = os.path.dirname(filePath)+"/ScreenerOutput.xlsx"
writer=ExcelWriter(newFile)
total_return_list.to_excel(writer,"Sheet1")
writer.save()

import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()

emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]

stock = input("Enter the stock ticker : ")
start_date = dt.datetime(2020,1,1)
end_date = dt.datetime.now()
df = pdr.get_data_yahoo(stock,start_date,end_date)
pos = 0
num = 0
capital = 50000
qty = 0
for i in emasUsed:
        ema=i
        df["{} EMA".format(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

print (df)

for i in df.index:

        percentchange=[]
        cmin = min(df["3 EMA"][i],df["5 EMA"][i],df["8 EMA"][i],df["10 EMA"][i],df["12 EMA"][i],df["15 EMA"][i])
        cmax = max(df["30 EMA"][i],df["35 EMA"][i],df["40 EMA"][i],df["45 EMA"][i],df["50 EMA"][i],df["60 EMA"][i])
        close = df["Adj Close"][i]
        num+=1
        if(cmin>cmax):
            #print("RWB Crossover")
            if(pos==0):
                bp=close
                pos=1
                qty = int(capital/bp)
                capital -= qty*bp
                print("Bought {} shares at {} on ".format(qty,bp)+str(i))
        elif(cmin<cmax):
            #print("Negative Crossover")
            if(pos==1):
                sp=close
                pos=0
                capital += qty*sp
                print("Sold {} shares at {} on ".format(qty,sp)+str(i))
                print("Capital = {}".format(capital))
                percentchange.append(((sp-bp)/bp)*100)
        if(num==df["Adj Close"].count() and pos==1):
            sp=close
            pos=0
            capital += qty*sp
            print("Sold {} shares at {} on ".format(qty,sp)+str(i))
            print("Capital = {}".format(capital))
            percentchange.append(((sp-bp)/bp)*100)
    #print("End Capital for {} is : {}".format(stock,capital))
    #print(percentchange)

treturn  = ((capital-50000)/50000)*100
print("Total Capital for {} is {} and total return is {}%".format(stock,capital,treturn))
    #print(df.count())

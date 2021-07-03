import pandas as pd
import numpy as np
from pandas import ExcelWriter
from smartapi import SmartConnect
from tkinter import *
from tkinter.filedialog import askopenfilename

obj = SmartConnect(api_key='565Evkhi')
data = obj.generateSession('A545511','Kite@666')

root = Tk()
filePath = askopenfilename()
root.withdraw()

nifty_500_list = pd.read_excel(filePath)

#print(nifty_500_list)

for x in nifty_500_list.index:
    share_name = nifty_500_list['Symbol'][x]
    df = pd.DataFrame(columns=['Date','Time','Open','High','Low','Close','Volume'])
    param = {'exchange':'NSE','symboltoken':str(nifty_500_list['Token'][x]),'interval':'ONE_HOUR','fromdate':'2021-06-21 09:15','todate':'2021-07-02 15:30'}
    share = obj.getCandleData(param)
    for i in share['data']:
        date,time=i[0].split('T')
        df = df.append({'Date':date,'Time':time,'Open':i[1],'High':i[2],'Low':i[3],'Close':i[4],'Volume':i[5]},ignore_index=True)
    try:
        for i in df.index:
            if df['Time'][i] == '10:15:00+05:30' and df['Date'][i] != '2021-06-21':
                percent_change = ((df['Close'][i]-df['Close'][i-1])/df['Close'][i-1])*100
                if percent_change >=5:
                    print("Breakout occured at {} on {}".format(share_name,df['Date'][i]))
    except:
        print("Exception")

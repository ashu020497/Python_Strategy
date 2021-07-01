import pandas as pd
import numpy as np
from pandas import ExcelWriter
import datetime as dt
import os
from tkinter.filedialog import askopenfilename

#filePath = askopenfilename(initialdir = "C://Users//ashu0//Desktop//Python")
nifty_50 = pd.read_excel('C://Users//ashu0//Desktop//Python//Output Folder//nifty500.xlsx')
angel_token = pd.read_excel('C://Users//ashu0//Desktop//Python//Output Folder//comprehensive_list.xlsx')

list = []
for i in nifty_50.index:
    list.append(nifty_50['Symbol'][i])

angel_nifty_df = pd.DataFrame(columns=['Symbol','Token'])
count = 0
for i in angel_token.index:
    if ('-EQ' in angel_token['symbol'][i]) & (angel_token['exch_seg'][i] == 'NSE'):
        name = angel_token['symbol'][i].replace('-EQ','')
        if name in list:
            count+=1
            angel_nifty_df = angel_nifty_df.append({'Symbol':name,'Token':angel_token['token'][i]},ignore_index=True)

writer = ExcelWriter('C://Users//ashu0//Desktop//Python//Output Folder//500list.xlsx')
angel_nifty_df.to_excel(writer,'Nifty 500 list')
writer.save()

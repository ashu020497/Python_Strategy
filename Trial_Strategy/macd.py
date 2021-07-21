import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from tkinter import *
from tkinter.filedialog import askopenfilename
import streamlit as st
import talib
from pandas_datareader import data as pdr

yf.pdr_override()

nifty_list_100 = pd.read_excel(r'C:\Users\ashu0\Desktop\Python_Strategy\Input_Files\100list.xlsx')
nifty_list_500 = pd.read_excel(r'C:\Users\ashu0\Desktop\Python_Strategy\Input_Files\500list.xlsx')
list = st.sidebar.radio('Choose a Nifty list',('Nifty 100','Nifty 500'))

if list == 'Nifty 100':
    tickers = nifty_list_100['Symbol'].sort_values().tolist()
else :
    tickers = nifty_list_500['Symbol'].sort_values().tolist()
symbol = st.sidebar.selectbox('Choose a nifty 50 share',tickers)
lookback = st.sidebar.selectbox('Choose your lookback period',[1,2,3,4,5,6,7,8,9,10])
frequency = st.sidebar.radio("Choose frequency",("Daily","Weekly"))
ticker = symbol+'.NS'
info = yf.Ticker(ticker).info
#st.subheader(info)


if frequency == 'Daily':
    duration = lookback
    sdate = dt.datetime.now() - dt.timedelta(duration*365)
    edate = dt.datetime.now()
    df = pdr.get_data_yahoo(ticker,sdate,edate)
    total_days = (lookback*365)
else :
    duration = lookback*7
    sdate = dt.datetime.now() - dt.timedelta(duration*365)
    edate = dt.datetime.now()
    total_days = (lookback*365)*7
    df = pdr.get_data_yahoo(ticker,sdate,edate)
    df = df.asfreq('W-FRI', method='pad')
df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df.Close, fastperiod=12, slowperiod=26, signalperiod=9)
final_df = pd.DataFrame(columns= ['Buy Date','Buy Price','Sell Price','Sell Date','Percentage Change','Capital'])
pos=0
capital = 100000
count = 0
active_time=0
for i in df.index:
    count = count+1
    if pos==0 and df['macdhist'][i]>0:
        buy_price = df['Close'][i]
        quantity = int(capital/buy_price)
        capital = capital - (buy_price*quantity)
        pos = 1
        buy_date = i.date()
        #st.markdown('Bought {} shares at {} on {}'.format(quantity,buy_price,i.date()))
    if pos == 1:
        max_drawdown = (df['Close'][i] - buy_price)/buy_price
        percentage_change = ((df['Close'][i]-buy_price)/buy_price)*100
    if pos==1 and (df['macdhist'][i]<0 or max_drawdown<-0.1):
        sell_price = df['Close'][i]
        capital = capital + sell_price*quantity
        pos = 0
        sell_date = i.date()
        active_time += (sell_date - buy_date).days
        #st.markdown('Sold {} shares at {} on {}'.format(quantity,sell_price,i.date()))
        percentage_change = ((sell_price-buy_price)/buy_price)*100
        final_df = final_df.append({'Buy Date':buy_date,'Buy Price':buy_price,'Sell Price':sell_price,'Sell Date':sell_date,'Percentage Change':percentage_change,'Capital':capital},ignore_index=True)

    if pos==1 and count==df['Close'].count():
        sell_price = df['Close'][i]
        capital = capital + sell_price*quantity
        percentage_change = ((sell_price-buy_price)/buy_price)*100
        sell_date = i.date()
        active_time += (sell_date - buy_date).days
        final_df = final_df.append({'Buy Date':buy_date,'Buy Price':buy_price,'Sell Price':sell_price,'Sell Date':sell_date,'Percentage Change':percentage_change,'Capital':capital},ignore_index=True)
        #st.markdown('Sold {} shares at {} on {}'.format(quantity,sell_price,i.date()))

if frequency == 'Daily':
    active_time += (sell_date - buy_date).days
else:
    active_time += (sell_date - buy_date).days
final_df.index += 1
total_return = capital/100000
annual_return = (pow(total_return,1/(duration))-1)*100
st.subheader('** Initial Capital ** : 100000')
st.subheader('** Final Capital ** : {}'.format(capital))
st.subheader('** Annual Return ** : ' + str(round(annual_return,3))+'%')
st.subheader('** Active Time ** : {} days out of {} days.'.format(active_time,total_days))
st.table(final_df)

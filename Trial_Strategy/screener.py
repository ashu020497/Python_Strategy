import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
nifty_50 = pd.read_excel(r'C:\Users\ashu0\Desktop\Python_Strategy\Input_Files\100list.xlsx')
symbols = nifty_50['Symbol'].sort_values().tolist()
list = st.sidebar.radio('Choose a Nifty list',('Nifty 100, Nifty 500'))
symbol = st.sidebar.selectbox('Choose a Nifty 100 stock',symbols)
ticker = symbol+'.NS'
infoType = st.sidebar.radio(
        "Choose an info type",
        ('Fundamental', 'Technical')
    )
if(infoType == 'Fundamental'):
        stock = yf.Ticker(ticker)
        info = stock.info
        st.title('Company Profile')
        st.subheader(info['longName'])
        st.markdown('** Sector **: ' + info['sector'])
        st.markdown('** Industry **: ' + info['industry'])
        st.markdown('** Phone **: ' + info['phone'])
        st.markdown('** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', '  +  info['country'])
        st.markdown('** Website **: ' + info['website'])
        st.markdown('** Business Summary **')
        st.info(info['longBusinessSummary'])
        fundInfo = {
            'Enterprise Value (USD)': info['enterpriseValue'],
            'Enterprise To Revenue Ratio': info['enterpriseToRevenue'],
            'Enterprise To Ebitda Ratio': info['enterpriseToEbitda'],
            'Net Income (USD)': info['netIncomeToCommon'],
            'Profit Margin Ratio': info['profitMargins'],
            'Forward PE Ratio': info['forwardPE'],
            'PEG Ratio': info['pegRatio'],
            'Price to Book Ratio': info['priceToBook'],
            'Forward EPS (USD)': info['forwardEps'],
            'Beta ': info['beta'],
            'Book Value (USD)': info['bookValue'],
            'Dividend Rate (%)': info['dividendRate'],
            'Dividend Yield (%)': info['dividendYield'],
            'Five year Avg Dividend Yield (%)': info['fiveYearAvgDividendYield'],
            'Payout Ratio': info['payoutRatio']
        }

        fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
        fundDF = fundDF.rename(columns={0: 'Value'})
        st.subheader('Fundamental Info')
        st.table(fundDF)

from smartapi import SmartConnect
import pandas as pd
from pandas import ExcelWriter

obj = SmartConnect(api_key="3UGR4i5t")

data = obj.generateSession("A545511","Kite@666")

user_profile = obj.getProfile(data['data']['refreshToken'])
feedToken=obj.getfeedToken()

print(user_profile)
param = {'exchange':'NSE','symboltoken':'8054','interval':'ONE_DAY','fromdate':'2021-01-01 09:15','todate':'2021-06-22 15:30'}
info = obj.getCandleData(param)

df = pd.DataFrame(columns=['Time','Open','High','Low','Close','Volume'])

for i in info['data']:
    x,y = i[0].split('T')
    df = df.append({'Time': x,'Open':i[1],'High':i[2],'Low':i[3],'Close':i[4],'Volume':i[5]},ignore_index=True)

#print(df)
writer = ExcelWriter('angel_output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

obj.terminateSession('A545511')

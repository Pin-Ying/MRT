import pandas as pd
import numpy as np
import json

url="Rain_data.json"

with open(url,encoding="utf-8") as file:
    data=json.load(file)

datas=data['cwaopendata']['resources']['resource']['data']['surfaceObs']

location=data['cwaopendata']['resources']['resource']['data']['surfaceObs']['location']

for d in location:
    # print(d["station"])
    if d["station"]['StationName']=="臺北":
        taipei_data=d
        
print(taipei_data)

df=pd.DataFrame(taipei_data['stationObsTimes']['stationObsTime'])

df.index=pd.to_datetime(df['Date'])
del df["Date"]

df["Rain"]=[bool(p['Precipitation']!="0.0") for p in df["weatherElements"]]
del df["weatherElements"]

time_list=["2024-01","2024-02"]
for when in time_list:
    df_get=df.loc[when]
    df_get.to_csv(f"Rain_{when}.csv",encoding="utf-8")

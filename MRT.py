import pandas as pd
import numpy as np
import MRT_tool
import matplotlib.pyplot as plt


# ### 用url取得資料(因為資料太大後來直接下載csv)

# MRT_URL = "https://data.taipei/api/frontstage/tpeod/dataset/resource.download?rid=eb481f58-1238-4cff-8caa-fa7bb20cb4f4"
# time_list=[202401,202402]
# total_data=pd.DataFrame([])
# 
# for when in time_list:
#     print(f'正在取得{when}資料...')
#     r=MRT_tool.get_url(MRT_URL,when)
#     print(f'已取得{when}資料')
#     
#     url_content=list(r.text.split())
#     for i in range(len(url_content)):
#         url_content[i]=list(url_content[i].split(","))
#     
#     df=pd.DataFrame(url_content[1:],columns=url_content[0])
#     
#     # 清除人次為0
#     df=df[(df["人次"]!="0")]
# 
#     # 將人次用成整數
#     df["人次"]=df["人次"].astype(int)
#     
#     # 將日期 的 type 轉換成 datetime
#     df["日期"]=pd.to_datetime(df["日期"])
#     total_data=pd.concat([total_data,df])

# ### 取得csv檔資料並轉成DataFrame

MRT_URL = "臺北捷運每日分時各站OD流量統計資料_202401.csv"
time_list=["202401","202402"]
total_data=pd.DataFrame([])

for when in time_list:
    url_content=f"臺北捷運每日分時各站OD流量統計資料_{when}.csv"
    with open(url_content,encoding="utf-8") as f:
        df=pd.read_csv(f)

    # 清除人次為0
    df=df[(df["人次"]!=0)]
    
    # 將日期 的 type 轉換成 datetime
    df["日期"]=pd.to_datetime(df["日期"])
    df.index=df["日期"]
    del df["日期"]

    total_data=pd.concat([total_data,df])

# ### 捷運站篩選

# 選擇捷運站
station_list=["圓山","東門","台北車站"]
total_station=[]

for station in station_list:
    print(f'正在取得{station}捷運站資料...')
    df_get=MRT_tool.df_get_station(total_data,station)
    print(f'已取得{station}捷運站資料')
    print(df_get)
    total_station.append(df_get)
print("資料擷取完成")


# ### 要分析哪站捷運站
# - 用st做為所選捷運站的ID
st=range(len(station_list))
st_=total_station[st[0]]

# ### 特定日期之進站出站量

df=st_.loc["2024-02-01"]

enter=df[df["進站"]==station_list[st[0]]]
leave=df[df["出站"]==station_list[st[0]]]

x=sorted(list(set(df["時段"])))
y1=[enter[(enter["時段"]==i)]["人次"].sum() for i in x]
y2=[leave[(leave["時段"]==i)]["人次"].sum() for i in x]


MRT_tool.plot_fig(f"{station_list[st[0]]}2024-02-01之進出站量","時間","總人數")

plt.xticks(np.linspace(0,23,24))

plt.plot(x,y1,"-o",x,y2,"-x")
plt.legend(["進站","出站"])

plt.show()


# ### 一次分析所有挑選捷運站/特定日期下的出入站量

time="2024-02-07"

MRT_tool.plot_fig(f"捷運站出入總人數{time} v.s. 時段(每小時)","時間","總人數")

plt.xticks(np.linspace(0,23,24))

plt_list=[]

for i in st:
    # print(total_station[st[i]])
    st_=total_station[st[i]]
    df=st_[st_.index==time]
    enter=df[df["進站"]==station_list[st[i]]]
    leave=df[df["出站"]==station_list[st[i]]]

    x=sorted(list(set(df["時段"])))
    y1=[enter[(enter["時段"]==i)]["人次"].sum() for i in x]
    y2=[leave[(leave["時段"]==i)]["人次"].sum() for i in x]

    
    plt.plot(x,y1,"-o",x,y2,"-x")
    plt_list.append(f"{station_list[st[i]]}進站")
    plt_list.append(f"{station_list[st[i]]}出站")

plt.legend(plt_list)
  
plt.show()

# ### 節日 vs 平日(二月/圓山)
# - x軸: 每小時
# - y軸: 每日平均人流出入量

st_=total_station[st[0]]
st_["節日"]=False

st_[(st_.index=="2024-02-01") & (st_["時段"]==8)]["人次"].sum()

### 直接將假日弄成list，並將每組日期帶入檢查是否為假日

hds=["03","04","08","09","10","11","12","13","14","17","18","24","25","28"]
st_["假日"]=[d.strftime("%d") in hds for d in st_.index]
st_[st_["假日"]==True]
# ### 使用 holidays 抓出台灣的節日

import holidays
tw_holidays = holidays.TW()
st_["節日"]=[d in tw_holidays for d in st_.index]
st_[st_.index=="2024-02"]

total_d=len(set(st_.index))

df_hd=st_[st_["節日"]==True]
df_nd=st_[st_["節日"]==False]

x=sorted(list(set(st_["時段"])))
y1=[df_hd[(df_hd["時段"]==i)]["人次"].sum()/len(tw_holidays) for i in x]
y2=[df_nd[(df_nd["時段"]==i)]["人次"].sum()/(total_d-len(tw_holidays)) for i in x]

MRT_tool.plot_fig("節日 vs 平日(一月+二月/圓山)","時間","平均人數")

plt.xticks(np.linspace(0,23,24))

plt.plot(x,y1,"-o")
plt.plot(x,y2,"-x")

plt.legend(["節日","平日"])

plt.show()


# ### 下雨是否影響捷運人潮?
# - 雨天 vs 無雨

df_rain=pd.read_csv("Rain_2024-02.csv",encoding="utf-8")

df_rain.index=pd.to_datetime(df_rain["Date"])
del df_rain["Date"]

rain_dates=df_rain[df_rain["Rain"]==True]

st_Feb=st_["2024-02":"2024-03"]

st_Feb["下雨"]=[df_rain.loc[d,]["Rain"] for d in st_Feb.index]

# 製圖

df_rd=st_Feb[st_Feb["下雨"]==True]
df_sd=st_Feb[st_Feb["下雨"]==False]

x=sorted(list(set(st_Feb["時段"])))
y1=[df_rd[(df_rd["時段"]==i)]["人次"].sum()/len(rain_dates) for i in x]
y2=[df_sd[(df_sd["時段"]==i)]["人次"].sum()/(29-len(rain_dates)) for i in x]

MRT_tool.plot_fig("雨天 vs 晴天(二月/圓山)","時間","平均人數")

plt.xticks(np.linspace(0,23,24))

plt.plot(x,y1,"-o")
plt.plot(x,y2,"-x")

plt.legend(["雨天","晴天"])

plt.show()


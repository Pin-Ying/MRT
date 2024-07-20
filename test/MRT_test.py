import MRT_tool
import pandas as pd
import matplotlib.pyplot as plt

# 臺北捷運各站進出量統計API => csv
MRT_URL = "https://data.taipei/api/frontstage/tpeod/dataset/resource.download?rid=eb481f58-1238-4cff-8caa-fa7bb20cb4f4"

# 選擇要查的年月
when=202310
print(f'正在取得{when}資料...')
r=MRT_tool.get_url(MRT_URL,when)
print(f'已取得{when}資料')

url_content=list(r.text.split())
for i in range(len(url_content)):
    url_content[i]=list(url_content[i].split(","))

df=pd.DataFrame(url_content[1:],columns=url_content[0])

# 將人次用成整數，並清除為0的資料
df["人次"]=df["人次"].astype(int)
df=df[(df["人次"]!=0)]

# 將日期 的 type 轉換成 datetime
df["日期"]=pd.to_datetime(df["日期"])

# 選擇要查的捷運站
station="圓山"
print(f'正在取得{station}捷運站資料...')
df_get=MRT_tool.df_get_station(df,station)
print(f'已取得{station}捷運站資料')

# 將時段排列
x=sorted(list(set(df_get["時段"])))
# 將此月分中每個時段人數加總，並產生 list
y=[df_get[(df_get["時段"]==i)]["人次"].sum() for i in x]

plt.figure(figsize=(12,6))

plt.xlabel('Time')
plt.ylabel('Total number of people')
plt.title("Yuanshan Station")

plt.plot(x,y,marker="o")

plt.show()

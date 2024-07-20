import requests as rq
import pandas as pd
import matplotlib.pyplot as plt


def get_url(MRT_URL,ym):
    # MRT_csv=list(csv.reader(rq.get(MRT_URL).text.split()))
    MRT_df = pd.read_csv(MRT_URL)
    MRT_df.index=MRT_df["年月"]
    url = MRT_df.loc[ym]["URL"]
    r = rq.get(url)
    if r.status_code==200:
        return r
    else:
        print("error",r.status_code)
        return None

def df_get_station(df,st):
    df_get=df[(df["進站"]==st) | ((df["出站"]==st) & (df["進站"]!=st))]
    return df_get

def plot_fig(tit="預設標題",xlab="預設x軸標題",ylab="預設y軸標題"):
    
    plt.figure(figsize=(12,6))
    
    plt.rcParams['font.family']='Microsoft YaHei'
    
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(tit)




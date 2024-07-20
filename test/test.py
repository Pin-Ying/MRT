import pandas as pd

list1=[[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
list2=[[1,1,1],[1,1,1]]
list3=[]

df1=pd.DataFrame(list1)
df2=pd.DataFrame(list2)

df=(pd.concat([df1,df2]))
list3.append(df1)
list3.append(df2)
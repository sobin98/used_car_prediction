import pandas as pd
import numpy as np

df_cars=pd.read_csv('cars.csv')

def changemodel(str1):
    index1 = str1.find(' ')
    index2 = str1.find(' ', index1 + 1)
    index3 = str1.find(' ', index2 + 1)
    return str1[:index3]

def changemodelname(str1):
    if '그랜져' in str1:
        str1 = str1.replace("그랜져", "그랜저")
        return str1
    else:
        return str1

def engine(str1):
    index=str1.find('cc')
    return str1[:index].replace(',','').rstrip()

def guar(str1):
    if str1=='만료' or str1=='불가':
        return pd.Series([0,0,0])
    elif str1=='정보없음':
        return pd.Series([np.nan,np.nan,np.nan])
    else:
        index=str1.find('/')
        if index==-1:
            time=0
        else:
            time=int(str1[:index-3].strip())
        km=str1[index+1:].replace(",","")[:-2].strip()
        return pd.Series([1,time,km])

matchop={'무':0,'유':1}
insurinfo={'미등록':0,'등록':1}
matchfuel={'디젤':0, 'LPG':1, '가솔린':2}


df_cars['이름'] = df_cars['이름'].apply(changemodel).apply(changemodelname)
df_cars['연식']=df_cars['연식'].apply(lambda x:x[:4]+x[5:7])
df_cars['주행거리']=df_cars['주행거리'].apply(lambda x:x.replace(",","")[:-2].rstrip())
df_cars['연료']=df_cars['연료'].replace(matchfuel)
df_cars['배기량']=df_cars['배기량'].apply(engine)
guartable=df_cars['보증정보'].apply(guar)
guartable.columns=['보증여부','보증기간','보증거리']
df_cars=pd.concat([df_cars,guartable],axis=1)
df_cars=df_cars.drop(['보증정보'],axis=1)
df_cars=df_cars.replace(matchop)
df_cars['보험이력등록']=df_cars['보험이력등록'].replace(insurinfo)
df_cars['보험_내차피해(가격)']=df_cars['보험_내차피해(가격)'].apply(lambda x: x.replace(",","") if isinstance(x,str) else np.nan)
df_cars['보험_타차피해(가격)']=df_cars['보험_내차피해(가격)'].apply(lambda x: x.replace(",","") if isinstance(x,str) else np.nan)

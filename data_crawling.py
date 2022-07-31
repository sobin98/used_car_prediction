import requests
from bs4 import BeautifulSoup
import pandas as pd
totalurl=[('https://www.bobaedream.co.kr/cyber/CyberCar.php?gubun=K&search_cat=C3_s0&maker_no=49&page={}&order=S11&view_size=70',3),
          ('https://www.bobaedream.co.kr/cyber/CyberCar.php?gubun=K&search_cat=C5_s10&maker_no=49&page={}&order=S11&view_size=70',3),
          ('https://www.bobaedream.co.kr/cyber/CyberCar.php?gubun=K&search_cat=C3_s0&maker_no=1010&page={}&order=S11&view_size=70',3),
          ('https://www.bobaedream.co.kr/cyber/CyberCar.php?gubun=K&search_cat=C5_s10&maker_no=1010&page={}&order=S11&view_size=70',3),
          ('https://www.bobaedream.co.kr/cyber/CyberCar.php?gubun=K&search_cat=C3_s0&maker_no=3&page={}&order=S11&view_size=70',3),
          ('https://www.bobaedream.co.kr/cyber/CyberCar.php?gubun=K&search_cat=C5_s10&maker_no=3&page={}&order=S11&view_size=70',3)]


df_cars=[]

urls=[]
for i in totalurl:
    pagenum=i[1]
    for j in range(pagenum):
        url=i[0].format(str(j))
        urls.append(url)

info=["이름","차량번호","링크","연식","주행거리","연료","배기량","색상","보증정보","가격","신차대비가격"]

coloptions=["옵션_선루프","옵션_파노라마선루프","옵션_열선앞","옵션_열선뒤","옵션_전방센서"
     ,"옵션_후방센서","옵션_전방캠","옵션_후방캠","옵션_어라운드뷰","옵션_네비순정"]

findoptions=["선루프","파노라마선루프","열선시트(앞좌석)","열선시트(뒷좌석)","전방센서"
     ,"후방센서","전방카메라","후방카메라","어라운드뷰","네비게이션(순정)"]
colacci_info1=["보험이력등록","소유자변경횟수","사고상세_전손","사고상세_침수전손","사고상세_침수분손","사고상세_도난","보험_내차피해(횟수)","보험_내차피해(가격)","사고상세_타차가해(횟수)","보험_타차피해(가격)"]


cols=info+coloptions+colacci_info1
    #링크추가: 아웃라이어인지 확인하기 위해

#옵션이름 받아서 있는지 없는지 확인
def option_check(soupobject,option_name):
    check = soupobject.find("button", text=option_name).find_parent().find_previous_sibling().get_attribute_list('checked')

    if check[0]=='':
        return '유'
    else:
        return '무'
#모든 url마다 실행

for url in urls:
    res=requests.get(url)
    res.raise_for_status()
    requests.adapters.DEFAULT_RETRIES = 10000
    soup=BeautifulSoup(res.text,"lxml")

    cars=soup.find_all("li",attrs={"class":"product-item"})
    links=[]
    #한 url마다 들어있는 모든 차들에 대해 실행
    for car in cars:
        link = "https://www.bobaedream.co.kr" + car.a["href"]
        links.append(link)
    for link in links:
        print(link)

        res2=requests.get(link,timeout=300)
        res2.raise_for_status()
        soup2 = BeautifulSoup(res2.text, "lxml")
        infobox = soup2.find("div", attrs={"class": "info-util box"})
        try:
            ratiopr = infobox.find("b")
        except:
            continue

        name=soup2.find("h3",attrs={"class":"tit"})
        state=soup2.find("div",attrs={"class":"tbl-01 st-low"})
        galdata=soup2.find("div",attrs={"class":"gallery-data"})
        carnumber=galdata.find("b")

        year=state.find("th",text='연식').find_next_sibling("td")
        km=state.find("th",text='주행거리').find_next_sibling("td")
        fuel=state.find("th",text='연료').find_next_sibling("td")
        amount=state.find("th",text='배기량').find_next_sibling("td")
        color=state.find("th",text='색상').find_next_sibling("td")
        guarn=state.find("b",text='보증정보').find_next("td")
        price=soup2.find("span",attrs={"class":"price"})

        option_table=soup2.find("div",attrs={"class":"tbl-option"})
        checkoptions=[]
        if option_table.find("th",text='외관')!=None:
            for option in findoptions:
                checkoptions.append(option_check(option_table,option))
        else:
            checkoptions=['']*len(coloptions)

        if infobox.find("span",attrs={"class":"round-ln insurance"}).find_next("i").find_next("em")==None:
            acc1 = '미등록'
        else:
            acc1 = '등록'


        findacci_info1=[]
        try:
            if acc1=='등록':
                acc1table=soup2.find("div",attrs={"class":"info-insurance"})
                insurdt1=acc1table.find("th",text="차량번호/소유자변경").find_next_sibling("td").get_text()[-2]
                insuraccis1 = acc1table.find("th", text="자동차보험 특수사고").find_next_sibling("td").get_text().split('/')
                insurdt2=insuraccis1[0][-2]
                insurdt3 = insuraccis1[1][-2]
                insurdt4 = insuraccis1[2][-2]

                insurdt5 = insuraccis1[3][-1]
                insuraccis2=acc1table.find("th", text="보험사고(내차피해)").find_next_sibling("td").get_text().split('회')
                insurdt6=insuraccis2[0]
                insurdt7=insuraccis2[1][2:-2]
                insuraccis3=acc1table.find("th", text="보험사고(타차가해)").find_next_sibling("td").get_text().split('회')
                insurdt8=insuraccis3[0]
                insurdt9=insuraccis3[1][2:-2]
                findacci_info1=[insurdt1,insurdt2,insurdt3,insurdt4,insurdt5,insurdt6,insurdt7,insurdt8,insurdt9]
            else:
                findacci_info1=['']*(len(colacci_info1)-1)
        except:
            findacci_info1 = [''] * (len(colacci_info1)-1)
        temp=[name.get_text(),carnumber.get_text(),link,year.get_text(),km.get_text(),fuel.get_text(),amount.get_text(),
          color.get_text(),guarn.get_text(),price.get_text(),ratiopr.get_text()]+checkoptions+[acc1]+findacci_info1
        df_cars.append(temp)
df_cars=pd.DataFrame(data=df_cars,columns=cols)
df_cars.to_csv('cardata.csv')
print(df_cars.head())

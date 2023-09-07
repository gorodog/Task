# all-con 사이트 웹크롤링

# requests, beautifulsoup 라이브러리 불러오기
import requests
from bs4 import BeautifulSoup

url = "https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

# 올콘 대외활동 페이지는 table 형식으로 정보가 정리돼 있어서 find로 table을 불러옴
a_list = soup.find('table')

# 컬럼헤더 가져오기
### 컬럼헤더는 thead 타입 안에 tr > th 타입으로 저장되어 있음
thead = a_list.find_all('th')

theadList = []

theadLen = len(thead)
for i in range(0,theadLen):
    thead = a_list.find_all('th')[i].text
    theadList.append(thead)
    
print(theadList)


# 컬럼바디 가져오기
### 가져와야하는 정보가 모두 저장되어 있는 부분
### tbody 타입 안에 tr > td 타입으로 저장되어 있음
tbody = a_list.find('tbody', {'id':'tbl-list'})

trData = tbody.find_all('tr')

tdData = trData[0].find_all('td') # index out of range 오류


# 수정해야함
rowList = []
columnList = []

trDataLen = len(trData)
for i in range(0,trDataLen):
    tdData = trData[i].find_all('td')
    
    tdDataLen = len(tdData)
    for j in range(0,tdDataLen):
        element = tdData[j].text
        columnList.append(element)

        rowList.append(columnList)
        columnList = []
    
print(rowList)



# pandas로 저장
import pandas as pd

result = pd.DataFrame(rowList, columns=theadList)
print(result)
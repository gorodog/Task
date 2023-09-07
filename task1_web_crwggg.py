import requests
from bs4 import BeautifulSoup

url = "https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

a_list = soup.find('table')

thead = a_list.find_all('th')

theadList = []

theadLen = len(thead)
for i in range(0,theadLen):
    thead = a_list.find_all('th')[i].text
    theadList.append(thead)
    
print(theadList)



tbody = a_list.find('tbody', {'id':'tbl-list'})

trData = tbody.find_all('tr')

tdData = trData[0].find_all('td')




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
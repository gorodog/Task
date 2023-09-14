### 흐름

1. 1차 코드 작성
2. 각종 오류
3. 2차 코드 작성 / 테이블 형식 도입
4. 각종 오류
5. Selenium 설치
6. 3차 코드 작성
7. 몇 개 수정/보완
8. 완료



***
### 1차 코드 작성



``` python
import requests
from bs4 import BeautifulSoup

url = "https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')


list = soup.select("#tbl-list")


activity_data = []


for lis in list:
    activity = lis.find_all("tr")
    for tr in activity:
       
        # # 별 붙은 항목이 있으면 이걸 따르고
        # if tr.select_one(".title is_star") in tr:
        #     tr_t_l = tr.select_one(".title is_star")
        #     # 타이틀    
        #     tr_title = tr_t_l.text
        #     # 링크
        #     tr_link = tr_t_l.get("href")
        #     # 카테고리
        #     tr_category = tr_t_l.select(".badge cl_cate")
           
           
        #     # 주최
        #     tr_held = tr.select_one(".host")
        #     # 모집기한
        #     tr_date = tr.select_one(".date")
       
       
        # 아니면 이걸 따르고
        #else:    
        tr_t_l = tr.select_one(".title")
        # 타이틀
        tr_title = tr_t_l.string
        # 링크
        tr_link = tr_t_l.get("href")
        # 카테고리
        tr_category = tr_t_l.select(".badge cl_cate")
       
           
        # 주최
        tr_held = tr.select_one(".host")
        # 모집기한
        tr_date = tr.select_one(".date")
           
        # tr_img = tr.select_one("")
       
       
    #저장
        activity_data.append({
            '제목':tr_title,
            '본문 링크':tr_link,
            '카테고리':tr_category,
            '주최':tr_held,
            '모집기한':tr_date
        })
        
   
import pandas as pd

file = pd.DataFrame(activity_data)

file.to_csv('대외활동_리스트.txt')

print(file)
```


***
### 각종 오류


1.  raise FeatureNotFound 오류

> 오류코드

``` python
raise FeatureNotFound(
bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?
```


> 해결 방법


``` python
pip install lxml
```


lxml을 설치해주면 해결된다.<br/>
애초에 beautifulsoup와 requests를 전부 설치하면서 lxml 혹은 html.parser을 함께 설치해야한다.


***
2. AttributeError: ResultSet object has no attribute 'find_all' 오류


``` python
a_list = soup.select(".tbl_head01 tbl_wrap")

lis = a_list.find_all('tr') # 오류 발생
for li in lis:
    host = li.select_one(".host").text
   
    title = li.select_one(".title")
    n_title = title.text
   
    print("호스트: ", host)
    print(n_title)
```


> 오류코드


``` python
AttributeError: ResultSet object has no attribute 'find_all'. You're probably treating a list of elements like a single element. Did you call 
find_all() when you meant to call find()?
```


> 해결 방법 

1.못 찾음<br/>
아마 tr은 table 형식에서 쓰는 거라 가져온 a_list가 잘못됐을 것 같다는 생각.<br/>
<br/>
<br/>
2. [BeautifulSoup find_all()과 find()의 차이점](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=dydgus092&logNo=221151686143)<br/>
<br/>
<br/>
3. for문 돌릴 때 함수명 실수로 발생하는 오류이므로 함수명 수정


``` python
for i in is:
  ap = is.find_all('a')
```


is.find_all이 아니라 i.find_all로 써야한다.


***
3. 출력값 1


``` python
soup = BeautifulSoup(res.text, 'lxml')

a_list = soup.select("tr")
print(len(a_list))
```


출력값: 1
<br>
<br>
tr을 th로 바꿔서 수행해도 같은 값이 나옴.
<br>

~~table로 받지 않아서 그런 것으로 추정...~~ 했으나 

<br>

**Selenium을 사용하여 웹페이지를 가져오지 않아서** 발생한 오류로 보임.


***
### 2차 코드 작성 / 테이블 형식 도입

[HTML tr tag](https://www.w3schools.com/tags/tag_tr.asp)

원래 하던 식과는 다른 방법으로 요소를 가져와야함.


<br/>

[HTML 테이블 구조 (Python 웹크롤링)](https://greendreamtrre.tistory.com/194)

이 포스트를 보고 코드 작성함. 올콘 페이지에 맞게 보완 필요.


``` python
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
```


### 각종 오류


1. IndexError:list index out of range 오류


``` python
tbody = a_list.find('tbody', {'id':'tbl-list'})
trData = tbody.find_all('tr')
tdData = trData[0].find_all('td') # IndexError:list index out of range 오류
```


2. AttributeError: ResultSet object has no attribute 'find_all'. You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?" 오류


``` python
trData = a_list.find_all('tr')
print(len(trData))
# 출력값 1 

tdData = trData.find_all('td') # AttributeError: ResultSet object has no attribute 'find_all'. You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?"
print(len(tdData))
```


3. trData가 비어 있음 <br><br> (출력값: <br> ['제목', '주최', '기간', '진행상황', '조회수'] <br> 아무것도 없음)


``` python
tbody = a_list.find('tbody', {'id':'tbl-list'})

trData = tbody.find_all('tr')

# trData 비어 있지 않으면 수행
if trData:
    print('있음')
    
# 비어 있을 때 수행
else:
    print('아무것도 없음')
```

출력값: '아무것도 없음'


2.5 AttributeError


``` python
tbody = a_list.find_all('tbody', {'id':'tbl-list'})

print(len(tbody))

trdata = tbody.find_all('tr')

print(len(tr))
```


#### 챗GPT

* * *
```
"ResultSet object has no attribute 'find_all'" 오류는 BeautifulSoup의 ResultSet 객체에서 find_all 메서드를 호출하려고 시도했을 때 발생하는 오류입니다. 이 오류는 주로 BeautifulSoup의 find_all 메서드를 적용해야 하는데 대상이 되는 HTML 요소를 찾지 못한 경우에 발생합니다.

먼저, 다음과 같은 점을 확인하십시오:

'tbody' 태그와 {'id': 'tbl-list'} 속성으로 요소를 찾은 결과가 tbody 변수에 할당되었는지 확인하세요.
trData 변수에는 tbody에서 찾은 모든 tr 요소들의 리스트가 들어가야 합니다.
```

``` python
# 컬럼바디 가져오기
tbody = a_list.find_all('tbody', {'id':'tbl-list'})

if tbody:
    # 'tr' 요소 찾기
    trData = tbody.find_all('tr')
    
    for tr in trData:
        tdData = tr.find_all('td')
        # 이제 tdData를 사용할 수 있습니다.
else:
    print("No tbody element with id 'tbl-list' found.")
```


ㄴ 수행 시

> AttributeError 발생


* * *
``` python
tbody = a_list.find_all('tbody', {'id':'tbl-list'})
tr_elements = tbody.find_all('tr')
```

#### 챗 GPT

* * *

tbody가 find_all 메서드를 호출하려는 시점에서 tbody는 ResultSet 객체가 아니라 list 객체입니다. 따라서 list 객체에는 find_all 메서드가 없기 때문에 해당 줄에서 오류가 발생합니다.

tbody가 ResultSet 객체가 아닌 list 객체로 반환된 이유는 soup.find_all('tbody', {'id':'tbl-list'}) 코드가 find_all 메서드를 호출하면서 해당 조건을 만족하는 모든 tbody 요소를 리스트로 반환했기 때문입니다.

따라서 tbody 요소의 리스트를 반복하고 각 요소에서 tr 요소를 찾으려면 다음과 같이 코드를 수정해야 합니다:


``` python
# <tbody> 요소를 찾습니다.
tbody_elements = soup.find_all('tbody', {'id': 'tbl-list'})

# 모든 <tbody> 요소를 반복합니다.
for tbody in tbody_elements:
    # 각 <tbody> 요소 내에서 <tr> 요소를 찾습니다.
    tr_elements = tbody.find_all('tr')
    
    # 찾은 <tr> 요소들을 순회하면서 처리할 수 있습니다.
    for tr in tr_elements:
        # 각 <tr> 요소에 대한 작업을 수행합니다.
        # 예를 들어, 각 <td> 요소에서 데이터를 추출하거나 출력할 수 있습니다.
```

해결되지 않음

***


``` python
# 컬럼바디에서 계속 오류가 나므로 컬럼바디만 가져오기

tbody = soup.select('table > tbody')

#컬럼바디에서 tr태그 가져오기
tr_elements = tbody.find_all('tr')

for tr in tr_elements:
    i = 1
    print (i)
    i+=1
```


또 AttributeError 오류 발생 <br>
= resultset 오류


``` python
# BeautifulSoup을 사용하여 HTML을 파싱합니다.
soup = BeautifulSoup(response.text, 'html.parser')

# 진행 중인 대외활동 수를 가져옵니다.
# 진행 중인 대외활동 수를 가져옵니다.
total_count_element = soup.find('span', string="진행중인 대외활동")
total_count = total_count_element.find_next('span').text.strip()


# 정렬 기준을 가져옵니다.
sortname_select = soup.find('select', id='sortname')
selected_option = sortname_select.find('option', selected=True).text

# 결과 출력
print("진행중인 대외활동 수:", total_count)
print("선택된 정렬 기준:", selected_option)
```


실행 결과:


``` python
16 total_count = total_count_element.find_next('span').text.strip()


AttributeError: 'NoneType' object has no attribute 'find_next'
```


AttributeError: 'NoneType' object has no attribute 'find_next' 에러 발생
***


``` python

# <table> 태그를 찾아서 가져오기
table = soup.find('table')

# <tbody> 태그를 찾아서 가져오기
tbody = table.find('tbody')

# 모든 <tr> 태그를 찾아서 반복 처리
for tr in tbody.find_all('tr'):
    # title 정보 가져오기
    # title = tr.find('td', class_='title').a.text.strip()
    td_elements = tr.find_all('td', class_='title')
    for td in td_elements:
        title = td.a.text.strip()
        print(title)
    
    # host 정보 가져오기
    host = tr.find('td', class_='host').text.strip()
    
    # date 정보 가져오기
    date = tr.find('td', class_='date').text.strip()
    
    # 결과 출력
    print("Title:", title)
    print("Host:", host)
    print("Date:", date)
    print()
```


ㄴ 결과 출력 X


``` python
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'lxml')
    
    table = soup.find('table')
    rows = table.find("tbody", {"id": "tbl-list"}).find_all("tr")
    for row in rows:
        # 제목, 주최, 기간, 진행상황, 조회수 정보를 추출합니다.
        title = row.find("td", class_="title").a.text.strip()
        host = row.find("td", class_="host").text.strip()
        date = row.find("td", class_="date").text.strip()
        status = row.find("td", class_="status").span.text.strip()
        view = row.find("td", class_="view").text.strip()

        print("제목:", title)
        print("주최:", host)
        print("기간:", date)
        print("진행상황:", status)
        print("조회수:", view)
        print("=" * 40)

else:
    print("페이지를 가져오지 못했습니다.")
```


ㄴ 결과 출력 X


* * *
문제 상황
1. tbody가 안 불러와짐(thead는 불러와짐)
2. find로 데이터를 불러왔는데 데이터가 값에 들어 있지 않은 상황
3. 계속되는 Attribute Error
4. 오류남
5. 안 됨

===> 챗GPT한테 도움 요청
* * *


#### 챗GPT
```
코드가 여전히 작동하지 않는다면 몇 가지 문제가 있을 수 있습니다. 아래의 단계를 따라가면서 문제를 해결해보세요:

1. 네트워크 접근 문제: 먼저 웹 사이트에 정상적으로 접근 가능한지 확인하세요. 브라우저를 사용하여 주어진 URL에 접속할 수 있는지 확인하고, 방화벽 등이 접근을 차단하고 있는지 확인하세요.

2. 라이브러리 버전 문제: requests와 BeautifulSoup 라이브러리의 버전이 호환되는지 확인하세요. 최신 버전을 사용하는 것이 좋습니다. 필요하다면 아래의 명령으로 업그레이드할 수 있습니다.

pip install --upgrade requests
pip install --upgrade beautifulsoup4

3. 코드 오류: 코드에 문법 오류나 오타가 있는지 다시 한 번 확인하세요.

4. 웹 사이트 변경: 웹 사이트가 변경되었거나 HTML 구조가 변경되었을 수 있습니다. 이 경우, 코드를 다시 조정해야 할 수도 있습니다.

5. 페이지 로딩 대기: 웹 사이트가 JavaScript를 사용하여 동적으로 데이터를 로드하는 경우가 있습니다. 이 경우 Selenium과 같은 도구를 사용하여 페이지 로딩을 기다리는 것이 필요할 수 있습니다.

6. 네트워크 요청 실패: 웹 페이지 요청이 실패할 경우 오류 메시지를 출력해보세요. `res.status_code` 값을 확인하여 요청이 성공적으로 이루어지는지 확인할 수 있습니다.

오류 메시지나 추가 정보를 제공하면 더 구체적인 도움을 드릴 수 있을 것입니다.
```

* * *
1. 네트워크 접근 문제 >>> 네트워크 연결 이상 X
2. 라이브러리 버전 문제 >>> 전부 최신 버전
3. 코드 오류 >>> 아무리 봐도 문제 X
4. 웹 사이트 변경 >>> 변경 X
5. 페이지 로딩 대기 >>> ...?
6. 네트워크 요청 실패 >>> XXX
* * *


#### 챗 GPT
```
웹 페이지가 JavaScript로 동적으로 데이터를 로드하는지 여부를 확인하려면 몇 가지 방법을 시도할 수 있습니다:

1. 페이지 로딩 중에 데이터가 나타나는지 확인: 웹 페이지를 열고 브라우저에서 페이지가 완전히 로드될 때까지 기다린 다음, 웹 페이지가 데이터를 표시하는지 확인합니다. 웹 페이지가 로딩 중에 데이터를 가져오는 경우, 페이지가 완전히 로드된 후에 데이터가 나타날 수 있습니다.

2. 웹 페이지 소스 코드 확인: 웹 페이지의 소스 코드를 보고 JavaScript 코드가 데이터를 동적으로 로드하고 있는지 확인할 수 있습니다. HTML 파일 내에서 JavaScript 코드를 검색하고, 이 코드가 데이터를 가져오는지 확인하세요. 데이터를 가져오는 데 사용되는 JavaScript 함수나 AJAX 호출을 확인할 수 있습니다.

3. 네트워크 탭 사용: 웹 브라우저의 개발자 도구를 열고 네트워크 탭을 확인합니다. 페이지를 새로고침하고 네트워크 탭에서 XHR(XMLHttpRequest) 또는 Fetch와 관련된 요청을 확인합니다. 이러한 요청이 페이지를 로드하는 동안 발생하면 데이터를 동적으로 가져오는 것일 가능성이 있습니다.

4. 웹 페이지를 크롤링하고 데이터 추출 시도: 웹 페이지가 데이터를 동적으로 로드하는 경우, Python과 Selenium 또는 Splash 같은 웹 자동화 도구를 사용하여 웹 페이지를 로드하고 데이터를 추출해 볼 수 있습니다. 이런 방식으로 웹 페이지가 동적으로 데이터를 가져오는지 확인할 수 있습니다.

5. 웹 페이지의 소스 코드 분석: 웹 페이지의 소스 코드를 자세히 분석하여 데이터를 가져오는 JavaScript 코드를 찾을 수 있습니다. JavaScript 함수나 이벤트 핸들러를 살펴보고, 데이터를 동적으로 로드하는 부분을 확인하세요.

데이터가 정적인 경우에는 웹 페이지의 소스 코드에 직접 데이터가 포함되어 있을 가능성이 높습니다. 그러나 데이터가 동적으로 로드되면 위의 방법 중 하나를 사용하여 확인할 수 있습니다.
```


#### 챗 GPT
```
네트워크 탭에서 XHR(XMLHttpRequest) 또는 Fetch와 관련된 요청을 확인하는 방법은 다음과 같습니다.

1. 브라우저 개발자 도구 열기:
   - 웹 페이지를 열고, 브라우저의 주소 표시줄에서 F12 키를 누르거나, 웹 페이지에서 마우스 오른쪽 버튼을 클릭한 후 "검사" 또는 "요소 검사"를 선택하여 개발자 도구를 엽니다.
   - 또는 브라우저 메뉴에서 "도구" 또는 "개발자 도구" 항목을 선택하여 개발자 도구를 엽니다.

2. 네트워크 탭 선택:
   - 개발자 도구가 열리면, 상단 메뉴 중 "네트워크" 또는 "Network" 탭을 선택합니다.

3. 페이지 새로고침:
   - 네트워크 탭을 선택한 후, 페이지를 새로고침하려고 웹 페이지에서 F5 키를 누르거나 브라우저의 새로고침 버튼을 클릭합니다.

4. XHR 또는 Fetch 요청 확인:
   - 네트워크 탭에서 페이지 로딩 중에 발생하는 네트워크 요청을 확인할 수 있습니다.
   - XHR(XMLHttpRequest) 요청은 "XHR" 또는 "XMLHttpRequest"로 표시되며, Fetch 요청은 "fetch"로 표시됩니다.
   - 이러한 요청을 클릭하면 해당 요청에 대한 자세한 정보 및 응답 데이터를 볼 수 있습니다.

5. 필터링:
   - 네트워크 탭에서 필요에 따라 필터링을 사용하여 XHR 또는 Fetch 요청만 표시할 수 있습니다. "XHR" 또는 "Fetch"를 필터로 사용하여 해당 요청만 표시할 수 있습니다.

네트워크 탭에서 이러한 단계를 따르면 XHR 또는 Fetch와 관련된 요청을 확인하고 해당 요청에 대한 세부 정보를 분석할 수 있습니다. 이를 통해 웹 페이지가 동적으로 데이터를 가져오는지 여부를 확인할 수 있습니다.
```


XHR 또는 Fetch 요청 확인하는 쪽에 뜬 걸 복사해서 GPT한테 보냈더니 이런 답변이 돌아옴


#### 챗 GPT
```
주어진 HTTP 요청을 보면 XHR(XMLHttpRequest) 요청이 사용된 것으로 보입니다. 이 요청은 웹 페이지에서 동적으로 데이터를 가져오는 데 사용되는 것이 일반적입니다. 이 경우, Selenium을 사용하여 웹 페이지를 크롤링하면 도움이 될 수 있습니다.

Selenium은 웹 페이지 상호작용 및 동적 컨텐츠 크롤링을 위한 도구로, 웹 브라우저를 제어하여 페이지를 로드하고 JavaScript가 실행되도록 하며, 요청을 수행하고 응답을 분석할 수 있습니다.

따라서 주어진 상황에서 웹 페이지에서 데이터를 가져와야 하는 경우, Selenium을 사용하는 것이 유용할 수 있습니다. Selenium을 사용하여 해당 페이지를 방문하고, XHR 요청을 통해 동적으로 로드되는 데이터를 추출할 수 있습니다. 이때 사용자 에이전트(User-Agent)나 쿠키 등의 요청 헤더를 설정하여 필요한 데이터를 가져올 수 있습니다.
```


XMLHttpRequest(XHR)은 AJAX 요청을 생성하는 JavaScript API입니다. XHR의 메서드로 브라우저와 서버간의 네트워크 요청을 전송할 수 있습니다.
[XHR (XMLHttpRequest)](https://developer.mozilla.org/ko/docs/Glossary/XMLHttpRequest)

* * *


===> 셀레니움 설치

[[Python] Selenium4 초기 설정 & 크롬 드라이버 자동 설치](https://velog.io/@hyosss/PYTHON-Selenium4-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%EC%84%A4%EC%A0%95)


> 셀레니움 사용하여 테이블 형식의 웹페이지 크롤링(=참고 코드)

[파이썬을 활용한 업무 자동화 3. 웹 크롤링 01. selenium 4](https://wikidocs.net/177133)
[[라인맨 포지션 평가] 웹 페이지 테이블 크롤링](https://velog.io/@eunsuh/%EB%9D%BC%EC%9D%B8%EB%A7%A8-%ED%8F%AC%EC%A7%80%EC%85%98-%ED%8F%89%EA%B0%80-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-%ED%85%8C%EC%9D%B4%EB%B8%94-%ED%81%AC%EB%A1%A4%EB%A7%81)


### 기본 세팅


``` python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


from webdriver_manager.chrome import ChromeDriverManager


service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```


### 다운로드


``` python
pip3 install webdriver-manager
pip3 install chromedriver_autoinstaller
```


* * *
### 3차 코드 작성


``` python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

import requests
from bs4 import BeautifulSoup

# import time

from webdriver_manager.chrome import ChromeDriverManager # 크롬드라이버 자동 업데이트

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)




driver.get("https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg=")
# time.sleep(1)  # ?

# 대기 시간 처리 / 암시적 대기
driver.implicitly_wait(1) # 1초


# Copy full XPath를 활용하여 테이블을 table 변수에 담음
table = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/table")

# 컬럼 헤더
# thead = table.find_element(By.TAG_NAME, 'th')

# theadList = []

# for i in range(0,5):
#     th = thead[i].text
#     theadList.append(th)


# 컬럼 바디
tbody = table.find_element(By.TAG_NAME, "tbody")

tr_elements = tbody.find_elements(By.TAG_NAME, "tr")


rowList = []
columnList = []

# i = 1
for index, value in enumerate(tr_elements):
    
    # # 태그 가져오기
    # tag_information = value.find_elements(By.TAG_NAME, "td")[0]
    # for ind, val in enumerate(tag_information):
    #     tag = val.find_elements(By.CSS_SELECTOR, "span").text
        
    # 타이틀
    title = value.find_elements(By.TAG_NAME, "td")[0].text
    # 주최
    host = value.find_elements(By.TAG_NAME, "td")[1].text
    # 접수기한
    date = value.find_elements(By.TAG_NAME, "td")[2].text
    # 하나의 td class="status" 항목 안에 <br>로 구분 되어 있음
    # split(엔터)로 분리해서 각각의 항목을 변수에 저장
    receiving = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[0] # 접수중 여부
    d_day = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[1] # 남은 디데이
    ### ongoing = str(receiving(d_day))
    # 조회수
    hits = value.find_elements(By.TAG_NAME, "td")[4].text
    
    # averageSalary = value.find_elements(By.TAG_NAME, "td")[-1].text.replace("$","").replace(",","")
    
    columnList.append([title, host, date, receiving, hits]) ### ongoing (개수 맞춰야됨) # i
    rowList.append(columnList)
    columnList = []
    # i += 1 # 랭킹 쓸 때 사용
    
    
# ?
# for row in columnList.iter_rows(max_col=5, values_only=True):
#     print(row)
    
theadList = ['제목', '주최', '기간', '진행상황', '조회수']

# pandas로 저장
import pandas as pd

result = pd.DataFrame(rowList, columns=theadList) # 바디, 헤더 순서
print(result)
```


#### PermissionError
``` python
"name": "PermissionError",
"message": "[WinError 5] 액세스가 거부되었습니다:


PermissionError: [Errno 13] Permission denied: 

PermissionError                           Traceback (most recent call last)


PermissionError: [WinError 5] 액세스가 거부되었습니다: 
```


> VSCode를 관리자 권한으로 실행해서 해결

* * *

일단 정상 작동함


``` python
# 컬럼 바디

''' rowList=[], columnList=[]를 tbodyList=[]로 수정 '''
tbodyList = []

for index, value in enumerate(tr_elements):
    # 타이틀
    title = value.find_elements(By.TAG_NAME, "td")[0].text
    # 주최
    host = value.find_elements(By.TAG_NAME, "td")[1].text
    # 접수기한
    date = value.find_elements(By.TAG_NAME, "td")[2].text
    # 하나의 td class="status" 항목 안에 <br>로 구분 되어 있음
    # split(엔터)로 분리해서 각각의 항목을 변수에 저장
    receiving = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[0] # 접수중 여부
    d_day = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[1] # 남은 디데이
    # 조회수
    hits = value.find_elements(By.TAG_NAME, "td")[4].text
    
    # 수정 전
    '''
    columnList.append([title, host, date, receiving, hits]) ### ongoing (개수 맞춰야됨) # i
    rowList.append(columnList)
    columnList = []
    '''
    # 수정 후
    tbodyList.append([title, host, date, receiving, hits])
```


                                                   제목             주최   
<br>
0                 미래내일일경험사업 2차 통합공고 청년 신청\n일반인대학생대학원생  고용노동부, 대한상공회…  \
<br>
1   (교육비 무료) 세계 AI 1위에게 배우는 Upstage AI Lab 교육생 모집\n기타         패스트캠퍼스   
<br>
2   2023 유산 해석·설명 청년 국제 역량강화 참여자 모집N\n\n기타(캠프/강연 등...  유네스코 세계유산 국제…   
<br>
3                트립코디 서포터즈 1기 모집N\n\n서포터즈·기자단·마케터제한없음           트립코디   
<br>
4   2023 1ㆍ3세대가 함께 온(溫) 세상을 만드는 '효행교육 페스티벌' 서포터즈 모...       대구광역시교육청   
<br>
5   홈플러스와 함께하는 ‘2023 두드림 페스티벌’ 자원봉사자 모집N\n\n봉사활동일반...  (사)스페셜올림픽코리아…   
<br>
6                    떡참 프렌즈 1기 모집N\n\n서포터즈·기자단·마케터대학생         기영에프앤비   
<br>
7      신한 커리어업 4기 참가자 모집N\n\n서포터즈·기자단·마케터 외일반인대학생대학원생  신한은행, 신한금융희망…   
<br>
8             제18회 부산불꽃축제 자원봉사자 모집N\n\n봉사활동일반인대학생대학원생          부산광역시   
<br>
9   부산IT교육센터 풀스텍&자바 개발자 취업대비반 수강생 모집N\n\n기타(캠프/강연 ...       부산IT교육센터   
<br>
10  삼성 갤럭시 스튜디오 캠퍼스 부산대학교 큐레이터 모집N\n\n서포터즈·기자단·마케터...             삼성   
<br>
11  브랜드저널리즘 콘텐츠크리에이터 2023-4기 모집N\n\n서포터즈·기자단·마케터일반...  (주)애드플래닛커뮤니케…   
<br>
12  icoop 자연드림 부산권역과 함께하는 굿네이버스 바른환경생활 시즌 6 참가자 모집...   굿네이버스 부산동부지부 
<br>
13  d·camp와 함께하는 워크넥트 광주 참여 스타트업 모집N\n\n기타(캠프/강연 등...  은행권청년창업재단 d·…   
<br>
14  2023 용마폭포문화예술축제 자원봉사자 '용마별' 모집N\n\n봉사활동일반인대학생대학원생         중랑문화재단   
<br>
<br>
                   기간  진행상황   조회수  
<br>                   
0   23.07.24~23.09.27   접수중  4225  
<br>
1   23.08.14~23.09.14   접수중  1997  
<br>
2   23.09.01~23.11.01   접수중    10  
<br>
3   23.09.13~23.09.26  접수예정    31  
<br>
4   23.09.01~23.09.21   접수중    22  
<br>
5   23.09.11~23.09.22   접수중    31  
<br>
6   23.09.12~23.09.24   접수중    72  
<br>
...
<br>
11  23.09.12~23.09.21   접수중    60  
<br>
12  23.09.12~23.10.03   접수중    59  
<br>
13  23.08.31~23.09.18   접수중    52  
<br>
14  23.09.08~23.10.05   접수중    54  


* * *

### 수정해야할 것
> #### 1. column 리스트 웹사이트에서 뽑아오기(컬럼 헤더)
지금 코드는 내가 column 리스트를 작성함 <br>
theadList = ['제목', '주최', '기간', '진행상황', '조회수']<br>
<br>

> #### 2. 제목, 태그
미래내일일경험사업 2차 통합공고 청년 신청\n일반인대학생대학원생<br>
<br>
\n뒤부터는 제목이 아니라 태그된 문자이므로 분리하여야함<br>
태그된 게 일반인, 대학생, 대학원생 으로 분리 되어야 하는데 띄어쓰기 되지 않고 출력<br>
span class="badge cl_cate"로 접근해서 하나씩 가져오게끔 코드 수정해야함<br>
<br>

> #### 3. 페이지 넘김
1페이지의 정보만 출력<br>
페이지에 들어가보면 누를 수 있는 페이지가 30페이지까지 있음<br>
=> 출력하고 싶은 페이지까지 출력할 수 있게 코드 작성<br>
<br>

> #### 4. 진행상황
접수중 여부랑 남은 디데이 합쳐서 진행상황열에 넣기<br>
현재는 접수중 여부만 진행상황에 들어가 있음<br>
<br>

> #### 5. 기타사항

``` python
import requests
from bs4 import BeautifulSoup
```

현재로는 사용 X

***

#### column을 웹사이트에서 가져오도록 수정한 코드


``` python
# 컬럼 헤더
# 이전에 작동 된 컬럼 헤더 호출 코드 추가

# 수정 전
'''
# print(theadList)
# theadList = ['제목', '주최', '기간', '진행상황', '조회수']
'''

# 수정 후
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
```

정상 작동 하긴 하나,
<br>
이전에 걸린 시간 12초, bs4를 import해서 컬럼헤더까지 뽑아오는데 걸린 시간 30초 <br>
=> 시간이 너무 많이 걸린다<br>
<br>

<br>
가져와서 column만 뽑아내는 건 좋지 않은 선택이라<br>
다른 방법 강구<br>


### 수정한 코드
``` python
# 수정 전
'''
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
'''

# 수정 후
thead = table.find_element(By.TAG_NAME, "thead")
theadList = []
for i in range(0,5):
    thead_elements = thead.find_elements(By.TAG_NAME, 'th')[i].text
    theadList.append(thead_elements)
```


걸린 시간: 12.4초<br>
<br>
수정해야할 것 중에서 <br>
1.첫번째 column 해결,<br>


### 제목에서 불필요한 요소 제거
```python
# 수정 전
    '''
    title = value.find_elements(By.TAG_NAME, "td")[0].text
    '''

# 수정 후
    title = value.find_elements(By.TAG_NAME, "td")[0].text.split("\n")[0].replace("N","")
```

2.두번째 제목 해결<br>
    - 불필요한 N, 불필요한 태그(ex 기타, 대학생 ...) 제거
2.두번째 태그 - column 쓸 게 딱히 마땅이 없어서 제외 > 해결<br>
<br>


### 문자열 결합

```python
# 수정 전
'''
    # 하나의 td class="status" 항목 안에 <br>로 구분 되어 있음
    # split(엔터)로 분리해서 각각의 항목을 변수에 저장
    receiving = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[0] # 접수중 여부
    d_day = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[1] # 남은 디데이
    ### ongoing = str(receiving(d_day))
'''

# 수정 후
    receiving = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[0] # 접수중 여부
    d_day = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[1] # 남은 디데이
    ongoing = receiving + ' / ' + d_day

    # ongoing 출력
    tbodyList.append([title, host, date, ongoing, hits])
```

4.https://zephyrus1111.tistory.com/290 < 문자열 결합 >>> 해결<br>
<br>


* * * 
~~### 추가한 것~~
<br>

~~1. 출력 개수 사용자 조절~~
~~y = int(input("출력하고 싶은 대외활동의 개수를 쓰시오.: "))~~
~~for index, value in enumerate(tr_elements[:y]):~~

~~다만 한 페이지에 담겨 있는 대외활동 수인 15개로 제한됨.~~

~~# for문 안에서 변수 생성 테스트~~

~~for i in range(1, 5):~~
    ~~globals()["a{}".format(i)] = i~~
    ~~print(a{i})~~

사용X

<br>
<br>

### 여전히 수정해야하는 사항 

> #### 3. 페이지 넘김
1페이지의 정보만 출력<br>
페이지에 들어가보면 누를 수 있는 페이지가 30페이지까지 있음<br>
=> 출력하고 싶은 페이지까지 출력할 수 있게 코드 작성<br>
<br>
* * *
#### 주의사항
1. 페이지 넘기면 맨 위의 대외활동 2개는 모든 페이지에서 똑같음 => 중복 제거
2. 페이지 넘기면 사이트 링크 바뀜
<br>
https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg=
<br>
여기서 contest/2/( 여기 숫자 )
<br>
숫자가 1~30까지 바뀜
<br>
=> https://bigdata-doctrine.tistory.com/34 카테고리별 네이버 기사 크롤링에서 사용한 링크 바꿔주는 함수 작성
<br>
<br>
for문마다 변수를 돌려서 각각의 데이터프레임에 저장한 후 마지막에 병합
<br>
https://trustyou.tistory.com/197 <<<
<br>
https://muzukphysics.tistory.com/225 <<< for문 안에서 변하는 변수 만드는 방법 (2개)
<br>
<br>

> #### 5. 기타사항
import requests<br>
from bs4 import BeautifulSoup<br>
현재로는 사용 X<br>


***
### 페이지 넘김, 데이터 병합을 수행하는 코드

``` python
# 추가된 부분

# 데이터를 병합해주는 함수
def concat(a):
    result = pd.concat([result, a])
    return

number = int(input("출력하고 싶은 대외활동의 페이지 수를 쓰시오.(최대 30): "))
for i in range(1,number+1):
    driver.get(f"https://www.all-con.co.kr/list/contest/2/{i}?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg=")



# 수정한 부분

    # 수정 전
    '''
    # pandas로 저장
    import pandas as pd

    result = pd.DataFrame(rowList, columns=theadList) # 바디, 헤더 순서
    print(result)
    '''


    # 수정 후

    # pandas로 저장

    # 전역변수 선언
        globals()["a{}".format(i)] = pd.DataFrame(data=tbodyList, columns=theadList)
        concat(["a{}".format(i)])
    
print(result)
```

에러 발생

> concat(["a{}".format(i)]) 
> 이 부분 코드가 제대로 안 먹히는 오류

<br>
<br>

### 수정

https://passwd.tistory.com/entry/Python-Pandas-%EB%B0%98%EB%B3%B5%EB%AC%B8%EC%9C%BC%EB%A1%9C-DataFrame-%ED%95%A9%EC%B9%98%EA%B8%B0<br>
^^^ 반복문으로 DataFrame 합치기<br>

``` python
# 수정 전
'''
# 전역변수 선언
        globals()["a{}".format(i)] = pd.DataFrame(data=tbodyList, columns=theadList)
        concat(["a{}".for
'''

# 수정 후
``` python
    if i == 1:
        result = pd.DataFrame(data=tbodyList, columns=theadList) # 바디, 헤더 순서
    if i != 1:
        # globals()['a{}'.format(i)] = pd.DataFrame(data=tbodyList, columns=theadList)
        a = pd.DataFrame(data=tbodyList, columns=theadList)
        concat(a)
```

<br>

에러 발생
``` python
UnboundLocalError: cannot access local variable 'result' where it is not associated with a value"
}
```
> 문제
전역변수 result가 제대로 선언되지 않은 문제

> 해결방법
concat 함수 전에 result를 선언해주어 해결

``` python
# 수정 전

'''
# 데이터를 병합해주는 함수
def concat(a):
    result = pd.concat([result, a])
    return
'''


# 수정 후

global result # result 초기화, 선언으로 해결

# 데이터를 병합해주는 함수
def concat(a):
    result = pd.concat([result, a])
    return
```


* * *

### 해야하는 것

~~1. 출력할 대외활동 광고? 개수 입력 받고 > 거기에 맞춰서 페이지 로드 , 출력~~
<br>
-> 개수보다 페이지 수로 하는 게 더 효과적일 것 같음

<br>


2. 중복 제거 [[Python] 데이터프레임 중복 제거 :: drop_duplicates](https://mizykk.tistory.com/93)

3. 본문 웹페이지 링크 출력


### 중복 제거

``` python
result_finish = result.drop_duplicates()
```

> 해결
result DataFrame의 중복을 제거하여 result_finish에 저장해서 해결


***
### 본문 웹페이지 링크 가져오기

``` python
    for index, value in enumerate(tr_elements):
        
        # 본문 링크
        link_on = value.find_elements(By.TAG_NAME, "a")
        link = link_on.get_attribute("href")
        
        
        tbodyList.append([title, host, date, ongoing, hits, link])
```

> 오류 발생
``` python
AttributeError: 'list' object has no attribute 'get_attribute'
```

> 문제
``` python
link_on = value.find_elements(By.TAG_NAME, "a")
link = link_on.get_attribute("href")
```

이 부분에서 두 번째 줄 get_attribute가 동작하지 않는다
<br>
<br>

> 해결 방안
한 줄로 코드 수정


``` python
# 수정 전
'''
link_on = value.find_elements(By.TAG_NAME, "a")
link_on.get_attribute("href")
'''

# 수정 후
link = value.find_element(By.TAG_NAME, "a").get_attribute('href')
```

<br>
<br>
<br>
<br>

성공~~~
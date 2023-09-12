# ALL-CON 사이트 웹크롤링
대학생·일반인 대외활동   
[link_all_con](https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg=)<br/>
<br/>


**※ 과제를 수행하며 발생한 이슈를 두서없이 작성한, 아직 정리되지 않은 초안입니다.**

<br/>

---

## 1.
처음엔 링커리어 사이트로 크롤링하려 했으나, 코드가 너무 복잡하여 사이트 변경   
<br/>

---

## 2. 사용 함수
().select_one(“   “)<br/>
().text<br/>
().get(“   “)<br/>
.find(“   “)<br/>
.find_all(“   “)<br/>
<br/>

---

## 3. raise FeatureNotFound 오류
```
import requests
from bs4 import BeautifulSoup

url = "https://news.naver.com/main/ranking/popularMemo.naver" 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
```
<br/>

> 오류코드

```
raise FeatureNotFound(
bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?
```

<br/>

> 해결 방법

```
pip install lxml
```

lxml을 설치해주면 해결된다.<br/>
애초에 beautifulsoup와 requests를 전부 설치하면서 lxml 혹은 html.parser을 함께 설치해야한다.<br/>

<br/>

---

## 4. AttributeError: 'NoneType' object has no attribute 'text' 오류
<br/>

---

## 5. dataFrame으로 저장
- dataFrame으로 변환

```
import pandas as pd

file = pd.DataFrame(newsData)
print(file)
```


<br/>

- dataFrame을 텍스트로 저장

```
import pandas as pd

df.to_csv('pizza.txt')
```

<br/>

---

## 6. lxml과 html.parser의 차이점
<br/>

---

## 7. beautifulsoup 명령어
1. [BeautifulSoup SELECT 정리 및 사용법](https://pythonblog.co.kr/coding/11/)<br/>
2. [[Python 크롤링] 2. Beautiful Soup, bs4 사용법, find(), find_all(), select()](https://parkjh7764.tistory.com/139)<br/>
3. [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)<br/>
<br/>

---

## 8. AttributeError: ResultSet object has no attribute 'find_all' 오류
```
import requests
from bs4 import BeautifulSoup


url = "https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}


res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')


a_list = soup.select(".tbl_head01 tbl_wrap")


lis = a_list.find_all('tr') # 오류 발생
for li in lis:
    host = li.select_one(".host").text
   
    title = li.select_one(".title")
    n_title = title.text
   
    print("호스트: ", host)
    print(n_title)
```
<br/>

> 오류코드
  
```
AttributeError: ResultSet object has no attribute 'find_all'. You're probably treating a list of elements like a single element. Did you call 
find_all() when you meant to call find()?
```
<br/>

> 해결 방법 

1.못 찾음<br/>
아마 tr은 table 형식에서 쓰는 거라 가져온 a_list가 잘못됐을 것 같다는 생각.<br/>
<br/>
<br/>
2. [BeautifulSoup find_all()과 find()의 차이점](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=dydgus092&logNo=221151686143)<br/>
<br/>
<br/>
3. for문 돌릴 때 함수명 실수로 발생하는 오류이므로 함수명 수정
   
```
for i in is:
  ap = is.find_all('a')
```

is.find_all이 아니라 i.find_all로 써야됨<br/>
<br/>

---

## 9. 가상요소
> ::after <br/>
> ::before

[CSS 가상 요소 "::before"와 "::after" 완벽 정리](https://blogpack.tistory.com/1025)

<br/>

<br/>

---

## 10. 출력값 1 이슈
```
import requests
from bs4 import BeautifulSoup

url = "https://news.naver.com/main/ranking/popularMemo.naver" 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

a_list = soup.select("tr")
print(len(a_list))
```
출력값: 1<br/>
<br/>
tr을 th로 바꿔서 수행해도 같은 값이 나옴.<br/>
table로 받지 않아서 그런 것으로 추정...<br/>
<br/>

---

## 11. 표 - html <table> tag 크롤링 
## ...

[HTML tr tag](https://www.w3schools.com/tags/tag_tr.asp)

<br/>

원래 하던 식과는 다른 방법으로 요소를 가져와야함.


<br/>

<br/>

[HTML 테이블 구조 (Python 웹크롤링)](https://greendreamtrre.tistory.com/194)

<br/>

이 포스트를 보고 코드 작성함. 올콘 페이지에 맞게 보완 필요.

<br/>

---
## 12. 참고용
```
tag_lst = [] for a in a_tag: if "href" in a.attrs: # href가 있는것만 고르는 것 
if (f"sid={sid}" in a["href"]) and ("article" in a["href"]):
tag_lst.append(a["href"])
```

```
import requests
from bs4 import BeautifulSoup

# 크롤링할 링커리어 페이지의 URL & 헤더
url = "[https://www.linkcareer.co.kr/](https://www.all-con.co.kr/list/contest/2/1?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg=)"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

# 웹페이지 내용을 가져오기
response = requests.get(url)

# HTTP 응답 코드를 확인하여 정상적으로 응답 받았는지 확인
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

else:
    print("HTTP 요청에 실패하였습니다. 응답 코드:", response.status_code)
```
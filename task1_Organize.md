# 1주차

## 1. 목표 사이트
링커리어(https://linkareer.com/list/intern?gclid=Cj0KCQjwmICoBhDxARIsABXkXlJlZAGt_Dy-1h6-DfBfDp-92-wbiK-3c--1z5vTkquOLp-Ru0IMJhUaAnVqEALw_wcB)
-> 대외활동 사이트 올콘 (https://www.all-con.co.kr/)
변경

<br>
<br>
<br>

## 2. 내가 공부한 crawling 기법들(특정 블로그에 적힌 여러가지 기법)
### BeautifulSoup
아래와 강의자료실에 있는 3개의 블로그에 나와 있는 코드를 참고하여 1차 코드를 작성, 후에 table 구조를 확인하며 전부 엎었다.
- ().select(“ “)
- ().select_one(“ “)
- ().text
- ().get(“ “)
- .find(“ “)
- .find_all(“ “)
- [How To Use BeautifulSoup's find_all() Method](https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/)
- [BeautifulSoup SELECT 정리 및 사용법](https://pythonblog.co.kr/coding/11/)
- [[Python 크롤링] 2. Beautiful Soup, bs4 사용법, find(), find_all(), select()](https://parkjh7764.tistory.com/139)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [웹크롤링 - BeautifulSoup에서 find와 select 사용하기](https://velog.io/@jisu0807/%EC%9B%B9%ED%81%AC%EB%A1%A4%EB%A7%81-BeautifulSoup%EC%97%90%EC%84%9C-find%EC%99%80-select-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0#:~:text=select()%EC%99%80%20select_one()%EC%9D%98%20%EC%B0%A8%EC%9D%B4,-select()%EC%99%80&text=%ED%95%9C%20%EA%B0%80%EC%A7%80%20%EB%8D%94%20%EB%8D%A7%EB%B6%99%EC%9D%B4%EC%9E%90%EB%A9%B4,%EB%B2%88%EC%A7%B8%20%EA%B2%B0%EA%B3%BC%EB%A7%8C%20%EB%B0%98%ED%99%98%ED%95%A9%EB%8B%88%EB%8B%A4)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

아래 두 개의 코드를 참고하여 2차 코드 작성, 후에 Selenium을 사용하며 전부 엎었다.
- [HTML tr tag](https://www.w3schools.com/tags/tag_tr.asp)
- [HTML 테이블 구조 (Python 웹크롤링)](https://greendreamtrre.tistory.com/194)

- lxml과 html.parser의 차이점
  - lxml이 html.parser보다 빠르게 동작한다. 이외에도 단일 구문 처리라던가, html로 마크업 되어 있지 않은 경우라던가... 많은 부분에서 유용해서 따로 lxml을 설치하여 사용한다.

***

### javascript 사용 확인 방법
개발자 도구 네트워크 탭에서 XHR 또는 Fetch 요청을 확인하면 javascript를 사용하는지 확인할 수 있다.
XHR(XMLHttpRequest) 요청은 "XHR" 또는 "XMLHttpRequest"로 표시되며, Fetch 요청은 "fetch"로 표시된다.
여기서 XHR은 AJAX 요청을 생성하는 javascript API이다.

***

### Selenium
- [[Python] Selenium4 초기 설정 & 크롬 드라이버 자동 설치](https://velog.io/@hyosss/PYTHON-Selenium4-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%EC%84%A4%EC%A0%95)
- Selenium4 설치(+크롬 웹 드라이버 다운로드)와 기본설정을 참고하였다.

***

##### 아래 두 개의 코드를 참고하여 3차 코드 작성.
<br>
<br>

- [웹 크롤링/selenium 4](https://wikidocs.net/177133)

<br>

참고 코드
``` javascript
driver.find_element(By.XPATH, '//button')
driver.find_element(By.ID, 'loginForm')
driver.find_element(By.LINK_TEXT, 'Continue')
driver.find_element(By.PARTIAL_LINK_TEXT, 'Conti')
driver.find_element(By.NAME, 'username')
driver.find_element(By.TAG_NAME, 'h1')
driver.find_element(By.CLASS_NAME, 'content')
driver.find_element(By.CSS_SELECTOR, 'p.content')
```
By. 뒤쪽의 명령어를 구분하여 사용하는 예시를 참고하였다.
해당 포스트 안에 
1. 전통 로케이터
2. 상대 로케이터
3. 요소(element)와 상호작용 하기
4. 요소(element) 정보 가져오기
의 기능을 소개하고 있어서, 이를 참고하였다.
<br>
<br>

- [[라인맨 포지션 평가] 웹 페이지 테이블 크롤링](https://velog.io/@eunsuh/%EB%9D%BC%EC%9D%B8%EB%A7%A8-%ED%8F%AC%EC%A7%80%EC%85%98-%ED%8F%89%EA%B0%80-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-%ED%85%8C%EC%9D%B4%EB%B8%94-%ED%81%AC%EB%A1%A4%EB%A7%81)

<br>

참고 코드
``` javascript
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # 크롬드라이버 자동업데이트
import time
import openpyxl



i = 1

rows = tbody.find_elements(By.TAG_NAME, "tr")
for index, value in enumerate(rows):
    displayName = value.find_elements(By.TAG_NAME, "td")[1].text.split("\n")[0]
    team = value.find_elements(By.TAG_NAME, "td")[1].text.split("\n")[1]
    officialPosition = value.find_elements(By.TAG_NAME, "td")[2].text
    averageSalary = value.find_elements(By.TAG_NAME, "td")[-1].text.replace("$","").replace(",","")
    
    sheet.append([i, displayName, team, officialPosition, averageSalary])
    i += 1
```
아래 코드에서 i(랭킹 번호)를 제외하고 
1.find_elements로 요소를 가져온 것, 
2.value.find_elements(By.TAG_NAME, "td)[1].text 를 이용해 텍스트를 가져온 것
을 활용하여 코드를 작성하였다.

<br>
<br>
<br>

## 3. 목표 사이트를 접근하기 위해서 수정한 코드 설명(Trial and Error)
### 1. 수정한 코드
### 2. 오류
### 3. 수정한 코드
### 4. 오류
### 5. 수정한 코드
### 6. 오류


<br>
<br>
<br>

## 4. 최종 DataFrame에 넣고, 저장
``` javascript
import pandas as pd

// DataFrame에 넣기
file = pd.DataFrame(activity_data)

// 텍스트 파일로 저장
file.to_csv('대외활동_리스트.txt')
// 엑셀 파일로 저장
result.to_csv('allcon_result_x.xls',encoding='utf-8-sig') 
// csv 파일로 저장
result.to_csv('allcon_result_c.csv',index=False,encoding='utf-8-sig') 
```

<br>
<br>
<br>

## 5. 데이터 크롤링 구상
### 구상 / 구현한 요소
1. 올콘 사이트에 등록된 대외활동 페이지 크롤링
2. 한 페이지에 15개의 글, 30페이지까지 존재 ==> 원하는 페이지까지 정보를 가져올 수 있게 for문으로 페이지 변경
3. 제목, 주최, 접수기한, 남은날짜, 조회수, 본문링크 가져오기
4. 이때 남은 날짜는 (접수중 여부 + 남은 디데이) 합쳐서 가져오기
5. 페이지 별 데이터 프레임으로 저장
6. 데이터 프레임 병합 (병합해주는 함수 작성)
7. 상위 2개 항목은 모든 페이지가 동일 >>> 중복 삭제
8. 최종 데이터 프레임 저장

***

### 구상 / 구현하지 못한 요소
1. 출력하고 싶은 대외활동 개수를 입력 받아서 크롤링
  - 개수보다 페이지 수로 불러오는 것이 더 효과적일 것으로 생각하여, 페이지 수를 입력하는 것으로 대체
2. 링커리어 사이트와 대외활동 비교
  - 링커리어 사이트가 너무 복잡하게 만들어져 있어서 실패
3. 각 대외활동 별로 본문에 접속해서 상세 데이터 모으기
  - 양식이 정형화 되어 있지 않아서 데이터 전처리가 필요하며, 정보를 이미지로 첨부한 경우도 있어 지금 구현하기에는 어려울 것이라 판단.
4. 올콘 사이트에서 대외활동과 공모전을 분리해서 둘 다 크롤링
  - 하려 했으나, 딱히 의미가 없는 것 같아 수행하지 않았다.
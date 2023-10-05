## 웹크롤링 코드

``` python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

from webdriver_manager.chrome import ChromeDriverManager # 크롬드라이버 자동 업데이트


from bs4 import BeautifulSoup
import requests
import re
import time


service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


'''
# 대기 시간 처리 / 암시적 대기
driver.implicitly_wait(1)
없어도 돌아감
'''

'''
구상
1. 연합뉴스 1페이지와 2페이지를 가져옴 > 뉴스 기사 40개
2. 각각의 기사 링크 들어가서(셀레니움)
3. 본문 전체 스크랩 (태그 <p>)
4. 텍스트 파일? 아니면 판다스?로 저장
'''

# 일단 첫번째 페이지

# 연합뉴스 최근 순
driver.get("https://www.yna.co.kr/news/1")

# Copy full XPath를 활용하여 <li>가 담긴 list를 li_list에 넣음
li_list = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/section/div[1]/ul")

# li 마다
# a href 태그에서 2번째 거(첫번째는 이미지 링크)

# 어쩌고 스크롤 존에서 p태그

li_li = li_list.find_elements(By.TAG_NAME, "li")

title_List = []
href_List = []

for index, value in enumerate(li_li):

    # 타이틀
    title = value.find_elements(By.TAG_NAME, "strong")[0].text
    
    # 링크
    li_href = value.find_elements(By.TAG_NAME, "a").get_attribute("href")[1]
    
    title_List.append(title)
    href_List.append(li_href)
    
print(title_List)
print(href_List)
```
### 1. AttributeError

<br/>

li_href = value.find_elements(By.TAG_NAME, "a").get_attribute("href")[1]

<br/>

**AttributeError**

: 'list' object has no attribute 'get_attribute'

<br/>

> 해결

<br/>

List로 된 걸 반복해야한다고 해서, 아래와 같이 코드 수정

``` python
# 링크
    li_href = value.find_elements(By.TAG_NAME, "a")
    for my_href in li_href:
        li_href_url = my_href.get_attribute("href")[1]
```

***

### 2. IndexError

<br/>

- --> 57

<br/>

title = value.find_elements(By.TAG_NAME, "strong")[0].text

<br/>

**IndexError**

: list index out of range

<br/>

> 해결

``` python
# 타이틀
    title = value.find_elements(By.TAG_NAME, "strong")
```

***

### 3. 텍스트 append 속성 X

``` python
#뉴스 본문 가져오기
    content = ""
    content_p=soup.find_all('p')
    for title in content_p:
        p = title.get_text()
        # 텍스트 합치기
        p_p = ' '.join(str(p))
        content.append(p_p)
        
    data_List.append([title, content])
```

> 리스트로 수정

``` python
#뉴스 본문 가져오기
    content = []
    content_p=soup.find_all('p')
    for title in content_p:
        p = title.get_text()
        # 텍스트 합치기
        p_p = ' '.join(str(p))
        content.append(p_p)
        
    data_List.append([title, content])
```

***

### 결과

<br/>

기사 타이틀

<br/>

0  [[(C) Yonhapnews], [[대표이사] 성기홍], [[편집인] 강의영]]  \

<br/>

1  [[(C) Yonhapnews], [[대표이사] 성기홍], [[편집인] 강의영]]

<br/>

```
                                              본문

```

0  [재 난 포 털, 기 사 제 보, 자 동 완 성   기 능 이   켜 져   있 습...

<br/>

1  [재 난 포 털, 기 사 제 보, 자 동 완 성   기 능 이   켜 져   있 습...

<br/>

## 챗GPT로 수정한 코드

``` python
from bs4 import BeautifulSoup
import requests

href_List = ["https://www.yna.co.kr/view/AKR20230922002600075?section=news", "https://www.yna.co.kr/view/AKR20230922002400091?section=news"]

# ConnectionError방지
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }

# 차트 column
column_List = ['기사 타이틀', '본문']


t_c = []
for i in href_List:
    original_html = requests.get(i,headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    
    #뉴스 제목 가져오기
    title = html.select("#articleWrap > div.content03 > header > h1")
    # list합치기
    title = ''.join(str(title))
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1,repl='',string=title)

    #뉴스 본문 가져오기

    content = html.select("#articleWrap > div.content01.scroll-article-zone01 > div > div > article")

    # 기사 텍스트만 가져오기
    # list합치기
    content = ''.join(str(content))
    
    #html태그제거 및 텍스트 다듬기
    content = re.sub(pattern=pattern1,repl='',string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2,'')
    
    t_c.append([title,content])



import pandas as pd

result = pd.DataFrame(data=t_c, columns=column_List) 
  
result   
```

결과
![img](https://github.com/gorodog/Task/blob/main/img/1_result.png)

***

# mecab 설치

<br/>


설치 과정

<br/>

1. eunjeon 설치

<br/>

[[NLP] 윈도우 Windows에서 Mecab 사용하기! (주피터 / VSCode / Colab 등등)](https://chasingdreams.tistory.com/106)

<br/>
<br/>

2. konlpy 설치

<br/>

[Computer/ML·DL·NLP
[이수안컴퓨터연구소] 자연어 처리 Natural Language Processing 기초 2 한국어 NLP (Feat. Windows에서 Mecab 사용하기!)]](https://chasingdreams.tistory.com/28?category=958134#herer)

<br/>

[KoNLPy 설치하기](https://konlpy.org/ko/latest/install/)

<br/>

[자바 환경 변수 설정하기](https://minstar0410.tistory.com/3)

<br/>

[Jpype - Download(다운로드)](https://codedragon.tistory.com/7610)

<br/>

[VS에서 파이썬 버전 정보 변경하는 법](https://velog.io/@heezeo/VS%EC%97%90%EC%84%9C-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B2%84%EC%A0%84-%EC%A0%95%EB%B3%B4-%EB%B3%80%EA%B2%BD%ED%95%98%EB%8A%94-%EB%B2%95)

<br/>

[[Python] 파이썬 여러 버전 설치하고 설치된 버전 확인하는 방법](https://hoohaha.tistory.com/90)

<br/>

[https://lifere.tistory.com/entry/파이썬Python-여러-버전이-설치되어-있는-경우-버전-지정해서-사용하기](https://lifere.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%ACPython-%EC%97%AC%EB%9F%AC-%EB%B2%84%EC%A0%84%EC%9D%B4-%EC%84%A4%EC%B9%98%EB%90%98%EC%96%B4-%EC%9E%88%EB%8A%94-%EA%B2%BD%EC%9A%B0-%EB%B2%84%EC%A0%84-%EC%A7%80%EC%A0%95%ED%95%B4%EC%84%9C-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)

<br/>

[파이썬 기본 실행 버전 변경하기 (환경 변수 설정)](https://velog.io/@jajubal/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EA%B8%B0%EB%B3%B8-%EB%B2%84%EC%A0%84-%EB%B3%80%EA%B2%BD%ED%95%98%EA%B8%B0)

<br/>
<br/>

3. mecab 설치

<br/>
.<br/>
.<br/>
.<br/>
<br/>
파이썬 버전 변경이 안 돼서 kiwi형태소분석기로 변경...

***

# kiwi형태소분석기

[Keybert와 kiwi형태소분석기를 사용하여 키워드추출 하기](https://datainclude.me/posts/Keybert%EC%99%80_kiwi%ED%98%95%ED%83%9C%EC%86%8C%EB%B6%84%EC%84%9D%EA%B8%B0%EB%A5%BC_%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC_%ED%82%A4%EC%9B%8C%EB%93%9C%EC%B6%94%EC%B6%9C_%ED%95%98%EA%B8%B0/)

``` python
# 명사 추출 함수
def noun_extractor(text):
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
            results.append(token)
    return results

nouns = noun_extractor(text)
print(nouns)
```

***

# 데이터 정규화, 클렌징

앞서 저장한 csv 파일을 불러와 텍스트만 분리하려 했으나, 리스트 형식으로 들어가 있어 분리가 불가능

> 원래 코드
``` python
#뉴스 제목 가져오기
    title = html.select("#articleWrap > div.content03 > header > h1")
    # list합치기
    title = ''.join(str(title))
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1,repl='',string=title)
    titles.append(title)
```

<br/>

> 수정 코드
``` python
#뉴스 제목 가져오기
    title = html.select("#articleWrap > div.content03 > header > h1")
    # list합치기
    ''' title = ''.join(str(title)) # 삭제한 부분 '''
    title = ''.join([title_t.get_text() for title_t in title]) # 추가한 부분
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1,repl='',string=title)
    titles.append(title)
```

***

# 단어 빈도수

[딥 러닝을 이용한 자연어 처리 입문 02. 텍스트 전처리(Text preproc… 02-04 불용어(Stopword)](https://wikidocs.net/22530)

``` python
# from kiwipiepy import Kiwi
# kiwi = Kiwi()

# text = "서랍...서랍.서랍.배고프다.나는.사과가 먹고 싶다.. 고구마피자. "

# # a = kiwi.tokenize(text)
# # print(a)

# a = kiwi.tokenize(text)
# print(a)

# # 명사 추출 함수
# def noun_extractor(text):
#     results = []
#     result = kiwi.analyze(text)
#     for token, pos, _, _ in result[0][0]:
#         # 한 글자도 제거해버리는구나...
#         if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
#             results.append(token)
#     return results

# nouns = noun_extractor(text)
# print(nouns)



from kiwipiepy import Kiwi
kiwi = Kiwi()

import pandas as pd

data = pd.read_csv('save_t.csv')

# print(data['본문'].dtypes)
# print(data['기사 타이틀'].dtypes)
# print(data['본문'].dtypes)


### csv로 저장한 파일 안에 텍스트로 정보가 들어가 있는 게 아니라, 리스트 형식을 정보가 저장되어 있어서 dtypes로 불러오지 못함.
### csv 저장 단계로 돌아가서 리스트 대신 텍스트로 정보를 저장하는 과정이 추가적으로 필요함.

text_data = data['본문']

text_data.to_csv('body_data.txt')




with open('body_data.txt', "r", encoding="UTF8") as file:
    file_content = file.read()



# 명사 추출 함수
def noun_extractor(text):
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        # 한 글자도 제거해버리는구나...
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
            results.append(token)
    return results

nouns = noun_extractor(file_content)
print(len(nouns))

# 불용어 제거 함수
def noun_garbage(text):
    
    stop_words = ["기자", "광고", "카카오톡", "제보", "페이지", "뉴스", "제공", "o", "연합뉴스", "연합", "관련", "기관"]
    result = []
    for word in text:
        if word not in stop_words:
            result.append(word)
    return result

nouns_2 = noun_garbage(nouns)
print(len(nouns_2))

word_freq = {}

# 단어 빈도수를 세는 반복문
for noun in nouns_2:
    if noun in word_freq:
        word_freq[noun] += 1
    else:
        word_freq[noun] = 1
        


# 빈도수가 높은 순서로 상위 N개의 단어를 출력합니다.
top_n = 20  # 상위 N개의 단어를 출력하려면 N을 변경하세요.
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
for word, freq in sorted_word_freq[:top_n]:
    print(f'{word}: {freq}번')

'''
실행결과:
7900
기자: 139번
중국: 51번
광고: 51번
카카오톡: 51번
o: 50번
kjebo.: 50번
송고: 50번
제보: 49번
페이지: 45번
뉴스: 43번
대표: 42번
미국: 37번
제공: 37번
연합뉴스: 36번
연합: 36번
반도체: 36번
관련: 35번
판매: 33번
사진: 31번
추석: 31번
'''
    
# 기자, 광고, 카카오톡, 제보, 페이지, 뉴스 <<< 제거

# > 불용어 제거 함수(앞)


```
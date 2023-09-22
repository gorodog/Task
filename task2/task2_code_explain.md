# 긴 문장 text data 수집

### 기본 설정

``` python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

from webdriver_manager.chrome import ChromeDriverManager # 크롬드라이버 자동 업데이트

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```
***

#### 구상
1. 연합뉴스 1페이지와 2페이지를 가져옴 > 뉴스 기사 50개 (셀레니움)
2. 각각의 기사 링크 들어가서 본문 전체 스크랩 (bs4)

***

### 실시간 정렬되는 뉴스의 1페이지와 2페이지의 <br>
### 뉴스 제목, 뉴스 링크 가져오기

``` python
# 연합뉴스 1페이지

driver.get("https://www.yna.co.kr/news/1")

# 뉴스 제목과 링크 추출
news_elements = driver.find_elements(By.CSS_SELECTOR, ".section01 .item-box01")

href_List = []
for news_element in news_elements:
    title = news_element.find_element(By.CSS_SELECTOR, "strong.tit-news").text
    link = news_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    # print(f"제목: {title}")
    # print(f"링크: {link}")
    href_List.append(link)


# 연합뉴스 - 2페이지
driver.get("https://www.yna.co.kr/news/2")

# 뉴스 제목과 링크 추출
news_elements = driver.find_elements(By.CSS_SELECTOR, ".section01 .item-box01")

for news_element in news_elements:
    title = news_element.find_element(By.CSS_SELECTOR, "strong.tit-news").text
    link = news_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    # print(f"제목: {title}")
    # print(f"링크: {link}")
    href_List.append(link)
    
# 두 개가 함께 href_List에 저장되어 있음
# print(href_List)
```

### 가져온 뉴스 링크를 이용해 각각의 뉴스 기사 페이지에 접속하여
### 뉴스 제목, 뉴스 본문 가져오기
```python
from bs4 import BeautifulSoup
import requests
import re


# ConnectionError방지
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }

# 차트 column
column_List = ['기사 타이틀', '본문']

# 기사의 링크를 담은 href_List를 for문으로 돌리면서 각각의 기사에 접속
# 차트 body
t_c = [] # 기사 각각의 제목과 본문을 담을 리스트
for i in href_List:
    original_html = requests.get(i,headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    
    #뉴스 제목 가져오기
    title = html.select("#articleWrap > div.content03 > header > h1")
    # 제목 합쳐서 텍스트로 저장
    title = ''.join([title_t.get_text() for title_t in title]) 
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1,repl='',string=title)

    #뉴스 본문 가져오기

    content = html.select("#articleWrap > div.content01.scroll-article-zone01 > div > div > article")

    # 기사 텍스트만 가져오기
    # list합치기
    # 수정 필요
    # content = ''.join(str(content))
    content = ''.join([content_t.get_text() for content_t in content]) 
    
    #html태그제거 및 텍스트 다듬기
    content = re.sub(pattern=pattern1,repl='',string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2,'')
    content = content.replace("\n",'.')

    # contents.append(content)
    
    t_c.append([title,content])

# print(titles)
# print(contents)
```

### 판다스로 저장
``` python
# 판다스로 저장
import pandas as pd

result = pd.DataFrame(data=t_c, columns=column_List) 
# 인덱스 정보 제외하고 저장
result.to_csv('save_t.csv', index = None)
```

***

# 텍스트 정규화, 토큰화, word cloud 시각화

### 기본 설정
``` python
from kiwipiepy import Kiwi
kiwi = Kiwi()
```


### 앞에서 판다스로 저장한 뉴스 제목, 뉴스 본문 데이터 가져오기
``` python
import pandas as pd

data = pd.read_csv('save_t.csv')

# 본문 데이터만 가져옴
text_data = data['본문']

# txt파일로 저장
text_data.to_csv('body_data.txt')



# 저장한 txt 파일 읽어오기
with open('body_data.txt', "r", encoding="UTF8") as file:
    file_content = file.read()
```

### 명사 추출 함수
``` python
# 명사 추출 함수
def noun_extractor(text):
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
            results.append(token)
    return results

nouns = noun_extractor(file_content)
```

### 불필요한 명사 제거 함수
``` python
# 불필요한 명사 제거 함수
def noun_garbage(text):
    
    stop_words = ["기자", "광고", "카카오톡", "제보", "페이지", "뉴스", "제공", "o", "연합뉴스", "연합", "관련", "기관"]
    result = []
    for word in text:
        if word not in stop_words:
            result.append(word)
    return result

nouns_2 = noun_garbage(nouns)
```

### 단어 빈도수 세기
``` python
word_freq = {}

# 단어 빈도수를 세는 반복문
for noun in nouns_2:
    if noun in word_freq:
        word_freq[noun] += 1
    else:
        word_freq[noun] = 1
```

### 빈도수가 높은 순서로 상위 N개 단어 출력
``` python
top_nouns = {}
top_n = 30  # 상위 N개의 단어를 출력하려면 N을 변경하세요.
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
for word, freq in sorted_word_freq[:top_n]:
    # print(f'{word}: {freq}번')
    top_nouns.setdefault(word, freq)
    
# print(top_nouns)
```

### word cloud 시각화
``` python
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
# from PIL import Image

wc = WordCloud (max_words=30,
           background_color='black',
           font_path= '/usr/share/fonts/truetype/nanum/NanumSquareR.ttf',
           colormap='rainbow',
           )
wc.generate_from_frequencies(top_nouns)
plt.figure(figsize=(8,8))
plt.imshow(wc)
plt.axis('off')
plt.savefig('wordcloud.png') #그림을 저장
plt.show()
```
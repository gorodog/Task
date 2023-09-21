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


service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


'''
구상
1. 연합뉴스 1페이지와 2페이지를 가져옴 > 뉴스 기사 50개 (셀레니움)
2. 각각의 기사 링크 들어가서 본문 전체 스크랩 (bs4)
'''


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


from bs4 import BeautifulSoup
import requests


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
    content = ''.join(str(content))
    
    #html태그제거 및 텍스트 다듬기
    content = re.sub(pattern=pattern1,repl='',string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2,'')

    # contents.append(content)
    
    t_c.append([title,content])

# print(titles)
# print(contents)


# 판다스로 저장
import pandas as pd

result = pd.DataFrame(data=t_c, columns=column_List) 
# 인덱스 정보 제외하고 저장
result.to_csv('ave_task2_crawling_content.csv', index = None)
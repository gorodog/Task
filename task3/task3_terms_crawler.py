
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)

from webdriver_manager.chrome import ChromeDriverManager # 크롬드라이버 자동 업데이트

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



# top50 문서 링크 가져오기
driver.get("https://terms.naver.com/")

top = driver.find_element(By.CLASS_NAME, 'content_list')
list = top.find_elements(By.TAG_NAME, "li")
urls = [] # url에 문서 링크 저장
for i in list:
    link = i.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    # bool = ['https://terms.naver.com/#ratingbutton-useful', 'https://terms.naver.com/#ratingbutton-want', 'https://terms.naver.com/#ratingbutton-quote', 'https://terms.naver.com/#ratingbutton-modify']
    urls.append(link)
    
set_urls = set(urls)


url = ['https://terms.naver.com/entry.naver?docId=1012210&cid=50221&categoryId=50232', 'https://terms.naver.com/entry.naver?docId=1023264&cid=50221&categoryId=50232', 'https://terms.naver.com/entry.naver?docId=1081705&cid=40942&categoryId=33748', 'https://terms.naver.com/entry.naver?docId=1113247&cid=40942&categoryId=33383', 'https://terms.naver.com/entry.naver?docId=1130598&cid=40942&categoryId=34057', 'https://terms.naver.com/entry.naver?docId=1136362&cid=40942&categoryId=33383', 'https://terms.naver.com/entry.naver?docId=1145129&cid=40942&categoryId=34211', 'https://terms.naver.com/entry.naver?docId=1149081&cid=40942&categoryId=34063', 'https://terms.naver.com/entry.naver?docId=1152015&cid=40942&categoryId=34068', 'https://terms.naver.com/entry.naver?docId=1153537&cid=40942&categoryId=34071', 'https://terms.naver.com/entry.naver?docId=1156058&cid=40942&categoryId=33383', 'https://terms.naver.com/entry.naver?docId=2140285&cid=51000&categoryId=51000', 'https://terms.naver.com/entry.naver?docId=2210288&cid=51088&categoryId=51088', 'https://terms.naver.com/entry.naver?docId=2845156&cid=62033&categoryId=62033', 'https://terms.naver.com/entry.naver?docId=3410311&cid=47322&categoryId=47322', 'https://terms.naver.com/entry.naver?docId=3569309&cid=58907&categoryId=58922', 'https://terms.naver.com/entry.naver?docId=3570058&cid=59015&categoryId=59015', 'https://terms.naver.com/entry.naver?docId=3651808&cid=58663&categoryId=59566', 'https://terms.naver.com/entry.naver?docId=5646398&cid=60406&categoryId=60406', 'https://terms.naver.com/entry.naver?docId=5646411&cid=60406&categoryId=60406', 'https://terms.naver.com/entry.naver?docId=5646424&cid=60406&categoryId=60406', 'https://terms.naver.com/entry.naver?docId=5646470&cid=60406&categoryId=60406', 'https://terms.naver.com/entry.naver?docId=565914&cid=46625&categoryId=46625', 'https://terms.naver.com/entry.naver?docId=5764011&cid=43667&categoryId=43667', 'https://terms.naver.com/entry.naver?docId=6478781&cid=67309&categoryId=67309', 'https://terms.naver.com/entry.naver?docId=926581&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926584&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926619&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926631&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926637&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926659&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926702&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926728&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926738&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926745&cid=51007&categoryId=51007', 
'https://terms.naver.com/entry.naver?docId=926763&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926829&cid=51007&categoryId=51007', 'https://terms.naver.cver?docId=926835&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926899&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926900&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926919&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926931&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926933&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926951&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=926973&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=927021&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=927125&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=927167&cid=51007&categoryId=51007', 'https://terms.naver.com/entry.naver?docId=927594&cid=51007&categoryId=51007']

# 텍스트 자료 추출
from bs4 import BeautifulSoup
import requests

# ConnectionError방지
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }


for i in url:
    original_html = requests.get(i,headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    
    title = html.find("h2", class_ ="headword").text.strip()


    summarys = html.find('dl', class_='summary_area')
    summary = ''.join([i.get_text() for i in summarys])
    
    
    with open(f"{title}", 'w', encoding='utf-8') as file:
        file.write(summary.replace(" ",""))
        
    '''
    # 본문 내용
    contents = html.find_all('p', class_='txt')
    
    for i in contents:
        # contents = html.find('p', class_='txt')
        content = ''.join([content_t.get_text(strip=True) for content_t in i])
        
        with open(f"{title}", 'a') as file:
            file.write(content)
    '''
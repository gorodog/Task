from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

from webdriver_manager.chrome import ChromeDriverManager # 크롬드라이버 자동 업데이트

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


import pandas as pd


# result 초기화, 선언
result = pd.DataFrame()

# 데이터를 병합해주는 함수
def concat(a):
    # 전역변수 선언
    global result
    result = pd.concat([result, a])
    return

number = int(input("출력하고 싶은 대외활동의 페이지 수를 쓰시오.(최대 30): "))
for i in range(1,number+1):
    driver.get(f"https://www.all-con.co.kr/list/contest/2/{i}?sortname=cl_order&sortorder=asc&stx=&sfl=&t=2&ct=&sc=&tg=")


    # 대기 시간 처리 / 암시적 대기
    driver.implicitly_wait(1) # 1초


    # Copy full XPath를 활용하여 테이블을 table 변수에 담음
    table = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/table")


    # 컬럼 헤더
    thead = table.find_element(By.TAG_NAME, "thead")
    theadList = []
    for i in range(0,5):
        thead_elements = thead.find_elements(By.TAG_NAME, 'th')[i].text
        theadList.append(thead_elements)
    # 웹페이지에 없는 column 추가
    theadList.append("본문 링크")
        

    # 컬럼 바디
    tbody = table.find_element(By.TAG_NAME, "tbody")
    tr_elements = tbody.find_elements(By.TAG_NAME, "tr")

    tbodyList = []


    for index, value in enumerate(tr_elements):
        
        # 타이틀
        title = value.find_elements(By.TAG_NAME, "td")[0].text.split("\n")[0].replace("N","")
        
        # 주최
        host = value.find_elements(By.TAG_NAME, "td")[1].text
        # 접수기한
        date = value.find_elements(By.TAG_NAME, "td")[2].text
        # 하나의 td class="status" 항목 안에 <br>로 구분 되어 있음
        # split(엔터)로 분리해서 각각의 항목을 변수에 저장
        receiving = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[0] # 접수중 여부
        d_day = value.find_elements(By.TAG_NAME, "td")[3].text.split("\n")[1] # 남은 디데이
        ongoing = receiving + ' / ' + d_day
        # 조회수
        hits = value.find_elements(By.TAG_NAME, "td")[4].text
        # 본문 링크
        link = value.find_element(By.TAG_NAME, "a").get_attribute('href')
        
        
        tbodyList.append([title, host, date, ongoing, hits, link])
    


    # pandas로 저장
    
    if i == 1:
        result = pd.DataFrame(data=tbodyList, columns=theadList) # 바디, 헤더 순서
    if i != 1:
        a = pd.DataFrame(data=tbodyList, columns=theadList)
        concat(a)
    # result.to_csv('allcon_result_x.xls',encoding='utf-8-sig') # 엑셀 파일로 저장
    # result.to_csv('allcon_result_c.csv',index=False,encoding='utf-8-sig') # csv 파일로 저장
    
# 중복제거 
result_finish = result.drop_duplicates()

# 엑셀 파일로 저장
# result_finish.to_csv('allcon_result_x.xls',encoding='utf-8-sig')

print(result_finish)
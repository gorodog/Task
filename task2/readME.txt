<< 수행한 사항 >>

    - 긴 문장 text data 수집
yeonhapnews_webcrawling 파일은 긴 문장 data로, 연합 뉴스 기사 50개를 크롤링하여 csv파일로 저장하는 코드이다.

save_task2_crawling_content는 위의 코드를 실행시켜 저장된 csv파일이다.

    - 정규화
data_Normalization은 데이터를 토큰화하기 전에 정규화를 진행하는 코드가 작성되어 있는 파일이다. 현재 csv파일에서 필요한 텍스트만 가져오는 단계를 수행 중이다.

    - 토큰화
text_before는 데이터 토큰화를 진행하는 코드를 시행중인 파일로, kiwipiepy(키위형태소 분석기)를 사용하였다. 현재 명사를 추출하는 코드가 작성되어 있다.

---

<< 아직 수행되지 않은 사항 >>

- 각 단어별 빈도를 count해서 word cloud 시각화

---

<< 추가/수정 해야하는 사항 >>

- trial and error 문서
- 정규화
import pandas as pd

data = pd.read_csv('save_task2_crawling_content.csv')

# print(data['본문'].dtypes)
print(data.dtypes)

### csv로 저장한 파일 안에 텍스트로 정보가 들어가 있는 게 아니라, 리스트 형식을 정보가 저장되어 있어서 dtypes로 불러오지 못함.
### csv 저장 단계로 돌아가서 리스트 대신 텍스트로 정보를 저장하는 과정이 추가적으로 필요함.
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

# 불?용어 제거 함수
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
top_nouns = {}
top_n = 30  # 상위 N개의 단어를 출력하려면 N을 변경하세요.
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
for word, freq in sorted_word_freq[:top_n]:
    # print(f'{word}: {freq}번')
    top_nouns.setdefault(word, freq)
    
# print(top_nouns)


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
    
    
    
# 기자, 광고, 카카오톡, 제보, 페이지, 뉴스 <<< 제거
'''
이건 이전 코드
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


word_freq = {}

# 단어 빈도수를 세는 반복문
for noun in nouns:
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
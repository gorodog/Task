from kiwipiepy import Kiwi
kiwi = Kiwi()

import pandas as pd

data = pd.read_csv('save_t.csv')

# 본문 데이터만 가져옴
text_data = data['본문']

# txt파일로 저장
text_data.to_csv('body_data.txt')



# 저장한 txt 파일 읽어오기
with open('body_data.txt', "r", encoding="UTF8") as file:
    file_content = file.read()



# 명사 추출 함수
def noun_extractor(text):
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
            results.append(token)
    return results

nouns = noun_extractor(file_content)
print(len(nouns))

# 불필요한 명사 제거 함수
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


# word cloud 시각화
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

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
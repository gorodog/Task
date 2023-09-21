from kiwipiepy import Kiwi
kiwi = Kiwi()

text = "그동안 하원 공화당은 재량 지출 총액을 두고 케빈 매카시 하원의장, 중도파, 강경파 간 이견이 있었다. 중도파는 인기가 많은 복지 프로그램 등을 삭감할 경우 내년 선거에 미칠 영향을 우려했지만, 강경파는 지출 총액을 2022년 수준인 1조4천700억달러로 줄이지 않는 한 어떤 예산안 처리도 지지하지 않겠다고 했다. 강경파는 소수이지만 매카시 의장에 대한 소환 투표 요구권을 가진 데다 공화당이 불과 10석 차이로 하원 다수당 지위를 유지하고 있어 숫자에 비해 과한 영향력을 행사해왔다. "

# a = kiwi.tokenize(text)
# print(a)

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
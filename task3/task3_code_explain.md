chroma DB를 활용하여 텍스트를 색인 & 검색하는 코드

## 설명
- txt 파일 대신 pdf 파일 색인
- pdf 파일: DBpia 컴퓨터 분야 논문 22개

<br/>

- CharacterTextSplitter 대신 RecursiveCharacterTextSplitter 사용
- HuggingFaceEmbeddings 중 intfloat/multilingual-e5-large 사용

<br/>

***

## 텍스트 분할
### 1. RecursiveCharacterTextSplitter

<br/>

기본 권장 텍스트 분할기는 RecursiveCharacterTextSplitter입니다. 이 텍스트 분할기는 문자 목록을 사용합니다. 첫 번째 문자 분할을 기반으로 청크를 생성하려고 시도하지만 청크가 너무 크면 다음 문자로 이동하는 식입니다. 기본적으로 분할하려는 문자는 다음과 같습니다.["\n\n", "\n", " ", ""]

<br/>

[Document transformers](https://python.langchain.com/docs/modules/data_connection/document_transformers/)

<br/>

### 2. CharacterTextSplitter

<br/>

이것이 가장 간단한 방법입니다. 이는 문자(기본적으로 "\n\n")를 기준으로 분할되고 문자 수로 청크 길이를 측정합니다.

<br/>

[Split by character](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/character_text_splitter)

***

## Embedding

- Embedding 쪽을 바꿔야 성능이 잘 나올 것 같아서 여러 개의 Embedding을 사용해보려고 시도 중(OpenAI 제외)

<br/>

### 1. InstructorEmbedding

<br/>

[hkunlp/instructor-large](https://huggingface.co/hkunlp/instructor-large)

<br/>

[[LangChain] No using OpenAI API RetrievalQA](https://bnmy6581.tistory.com/197) - Instructor-xl

``` python
instructor_embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
```
코드 작성했으나, 런타임 에러 발생 

<br/>

### 2. LlamaCppEmbedding

<br/>

[Llama-cpp](https://python.langchain.com/docs/integrations/text_embedding/llamacpp)

``` python
llama = LlamaCppEmbeddings(model_path="/path/to/model/ggml-model-q4_0.bin")
```
model_path부분에서 오류 발생

[TheBloke/LLaMa-13B-GGML](https://huggingface.co/TheBloke/LLaMa-13B-GGML)

<br/>

### 3. intfloat/multilingual-e5-largeEmbedding

<br/>

intfloat/multilingual-e5-large Embedding 모델은 94개국어의 텍스트를 임베딩하는 모델이다.

<br/>

[Embedding으로 Llama2 응답 보정하기 (feat. langchain)](https://breezymind.com/llamacpp-embedding/)

<br/>

### 4. word2vec / fastText

<br/>

[Word2vec 및 fastText 임베딩 모델의 성능 비교](http://journal.dcs.or.kr/_PR/view/?aidx=24875&bidx=2056)

<br/>

[Word2vec 튜토리얼](https://www.tensorflow.org/text/tutorials/word2vec)

<br/>
<br/>

***

[임베딩에 관한 질문](https://www.reddit.com/r/LangChain/comments/14gbjly/question_on_embeddings/?rdt=61885)

<br/>

생싱•3개월 전

<br/>

https://huggingface.co/spaces/mteb/leaderboard

<br/>

word2vec 및 glove는 텍스트 임베딩이 아닌 워드 임베딩입니다. Bert는 전체 텍스트에 대한 임베딩이 아닌 각 토큰에 대한 임베딩을 제공합니다.

<br/>

SBERT는 문장 임베딩을 만들기 위해 BERT에서 토큰 임베딩의 econd 마지막 또는 마지막 레이어의 평균을 취한다고 생각합니다.

<br/>

임베딩이 어떤 용도로 사용되는지 이해하려면 다음을 읽으십시오. 많은 예제 코드가 있습니다.

<br/>

https://www.sbert.net/

<br/>

https://www.pinecone.io/learn/

***

## 코드

``` python
!pip install langchain unstructured openai chromadb Cython tiktoken pypdf

!pip install sentence-transformers

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader 
```

### pdf 파일을 로드하기 위해 추가
``` python
from langchain.document_loaders import PyPDFDirectoryLoader
```

``` python
from langchain.document_loaders import TextLoader 
from langchain.document_loaders import DirectoryLoader 

from langchain.vectorstores import Chroma #Vectorstore중 Chroma

from langchain.embeddings import HuggingFaceEmbeddings # HuggingFace 사용
```
### intfloat/multilingual-e5-large 임베딩 사용
``` python
# embeddings = HuggingFaceEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
```

``` python
#구글드라이브 마운트하기
from google.colab import drive
drive.mount('/content/drive')

# 업로드하고 실행해야함
fn_dir = "/content/drive/My Drive/Colab Notebooks/data/pdf_text_c" # PDF 파일
```

### txt대신 pdf파일 디렉토리 로드 

``` python
loader = PyPDFDirectoryLoader(fn_dir)

documents = loader.load()
```

### 텍스트 분할

``` python
# ↓ 1차 수정 ↓ 
text_splitter = CharacterTextSplitter(separator = "\n", chunk_size=1000, chunk_overlap=500) 

# ↓ 2차 수정 // CharacterTextSplitter 대신 RecursiveCharacterTextSplitter 사용 ↓
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) 
```

``` python
docs = text_splitter.split_documents(documents)

len(documents), len(docs)



db = Chroma.from_documents(docs, embedding=embeddings,
                                 persist_directory=".")
db.persist()



query = "인공지능은 어떻게 발전해왔는가?"
docs = db.similarity_search(query)



docs[:5]
```

## 실행 결과


### 1. HuggingFaceEmbedding()

<br/>

Chroma에 업로드 하는 데 걸린 시간: 32분

<br/>

실행 결과: 

<br/>

[Document(page_content='일자리인터넷관련일자리증가예상.\n․중장기적으로공유사회로일자리가옮겨갈\n것.공유사회에서는기계가인간을대체하\n는비중이더낮고사회적참여와사회적\n자본을축척하려면본질적으로인간이주\n체가될수밖에없어\n․비영리부문․자아실현욕구가커지면서장인,조언가,\n상담가,심리학자등에대한수요가늘어\n날것\n없어질\n일자리․재화,서비스생산에필요한인력이줄어들것․단순작업일자리뿐만아니라전문성과지식\n을겸비한화이트칼라일자리마저기계로\n대체\n․벽돌을쌓는작업이나,잔디를깎는일뿐만\n아니라엑스레이를읽거나단순한뉴스를\n쓰는,한마디로목표가확실하고목표를이\n루는수단이확실한직업이자동화될것\n자아실현\n욕구자아실현\n욕구발현․자신의재능공유하는데기쁨을느낌.․매슬로우5단계설과산업혁명관계흥미\n롭고말이됨.자아실현욕구커질것\n새로운\n소비자\n욕구․문화적활동에몰두.초월적인목표를추구\n․협업소셜공간에서활동하는세대는오픈\n소스공유체와같이비영리부문에서자\n신의재능을공유하고사회적으로연결된\n것에기쁨을느낌\n․큰네트워크공동체를위해자신이할수\n있는일을하는것이전체그룹의가치를', metadata={'page': 16, 'source': '/content/drive/My Drive/Colab Notebooks/data/pdf_text_c/제4차 산업혁명이 일자리에 미치는 영향.pdf'}),

<br/>

Document(page_content='일자리인터넷관련일자리증가예상.\n․중장기적으로공유사회로일자리가옮겨갈\n것.공유사회에서는기계가인간을대체하\n는비중이더낮고사회적참여와사회적\n자본을축척하려면본질적으로인간이주\n체가될수밖에없어\n․비영리부문․자아실현욕구가커지면서장인,조언가,\n상담가,심리학자등에대한수요가늘어\n날것\n없어질\n일자리․재화,서비스생산에필요한인력이줄어들것․단순작업일자리뿐만아니라전문성과지식\n을겸비한화이트칼라일자리마저기계로\n대체\n․벽돌을쌓는작업이나,잔디를깎는일뿐만\n아니라엑스레이를읽거나단순한뉴스를\n쓰는,한마디로목표가확실하고목표를이\n루는수단이확실한직업이자동화될것\n자아실현\n욕구자아실현\n욕구발현․자신의재능공유하는데기쁨을느낌.․매슬로우5단계설과산업혁명관계흥미\n롭고말이됨.자아실현욕구커질것\n새로운\n소비자\n욕구․문화적활동에몰두.초월적인목표를추구\n․협업소셜공간에서활동하는세대는오픈\n소스공유체와같이비영리부문에서자\n신의재능을공유하고사회적으로연결된\n것에기쁨을느낌\n․큰네트워크공동체를위해자신이할수\n있는일을하는것이전체그룹의가치를', metadata={'page': 16, 'source': '/content/drive/My Drive/Colab Notebooks/data/pdf_text_c/제4차 산업혁명이 일자리에 미치는 영향.pdf'}),

<br/>

... 이하 생략]

<br/>

***

### 2. intfloat/multilingual-e5-largeEmbedding()

<br/>

Chroma에 업로드 하는 데 걸린 시간: 1시간 15분

<br/>

실행 결과: 

<br/>

[Document(page_content='1) 인공지능의 정의 \n인공지능이란 인간의 지능으로 할 수 있는 사고와 학습 등을 \n기계를 통해 실현한 기술로써 기계가 인간과 같은 생각과 판단\n을 할 수 있게 하는 컴퓨터 정보기술의 한 분야이다 [5]. 이는 지\n각, 인지, 추론 등 인간의 능력들을 기술로서 대체할 수 있음을 \n의미한다 . 이와 같은 양상은 이미 우리 주변에서 쉽게 찾아 볼 \n수 있다. 우리 주변에서 쉽게 찾아 볼 수 있고 활용되고 있는, 오\n늘날의 인공지능을 ‘약한 인공지능 ’이라 일컫는다 . 상술된 바\n와 같이 어떤 문제를 실제로 사고하고 해결할 수 있고, 스스로\n의 지각과 인식 능력을 갖춘 ‘강한 인공지능 ’으로 발전하고 있\n으며 이에 관한 지속적인 연구가 진행되고 있다[6]. 이와 같은 \n인공지능의 개발 및 발전은 단순히 인간의 편의성을 증대시키\n는 것에 그치지 않고, 기존의 산업 구조 뿐 아니라 우리들의 삶 \n자체에 중대한 영향을 끼칠 것으로 예측된다 .\n2) 인공지능의 특징', metadata={'page': 2, 'source': '/content/drive/My Drive/Colab Notebooks/data/pdf_text_c/4차 산업 혁명 시대에서 인공지능(AI)의 작품 창작에 관한 연구 -예술인들의 인식을 중심으로-.pdf'}),

<br/>

 Document(page_content='친 개념이었을 것이다 . 이러한 새로운 경험은 사람의 \n머리와 마음에서 일어나는 일들을 진지하게 고찰하게 \n되는 계기로 작용하였다 . 즉, 사람의 머리에서 일어나\n는 일들도 수학 , 물리 , 화학처럼 “기계적 계산 과정 ”\n을 통해 설명할 수 있을 것이라는 생각으로 발전되었\n고, 결국 “마음은 정보처리과정의 산물이다 .”라는 생\n각이  시작되었다 . 이것이 곧 인지과학 (Cognitive Science) \n그리고 인공지능 (Artificial Intelligence, AI) 의 시작이\n다[1].\n2. 규칙기반 인공지능\n사람의 ‘지적 능력 ’과 연관된 능력을 이해하고 , 기\n계에 부여하려는 모든 시도를 인공지능이라고 할 수 \n있다 . 그렇기 때문에 인간의 지능을 어떻게 바라볼 것\n인가에 대한 생각의 차이가 중요한 철학적 , 기술적 차\n이를 만들어 낸다 . \n1950년대의 연구자들은 지능을 기계적 계산과정으\n로 설명할 수 있다는 “계산주의 ”에 근간하여 연구를', metadata={'page': 0, 'source': '/content/drive/My Drive/Colab Notebooks/data/pdf_text_c/인공지능과 심층학습의 발전사.pdf'}), 
 
 <br/>
 
 ... 이하 생략]

***

### 3. InstructorEmbedding

***

### 4. LlamaCppEmbedding
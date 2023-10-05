## embedding

종류: https://python.langchain.com/docs/integrations/text_embedding/

<br/>

query = “당뇨병에 걸리면 어떤 증상이 있어?”

***
### 0. HuggingFaceEmbeddings

<br/>

에러 <br/>

InvalidDimensionException: Embedding dimension 768 does not match collection dimensionality 1024

- 해결 방법 - 런타임 연결 해제 및 삭제하고 실행하니까 에러 안 남
- DB 업데이트에 걸린 시간: 1분

![0](img/0.HuggingFace.png)

***

### 1. intfloat/multilingual-e5-large

- embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
- DB 업데이트에 걸린 시간: 4분

![1](img/1.intfloat.png)

***

### 2. GPT4All

- !pip install gpt4all > /dev/null
- from langchain.embeddings import GPT4AllEmbeddings
- embeddings = GPT4AllEmbeddings()

에러

``` python
embeddings = GPT4AllEmbeddings()

db = Chroma.from_documents(docs, embedding=embeddings,
                                 persist_directory=".")
db.persist()
```

InvalidDimensionException: Embedding dimension 384 does not match collection dimensionality 1024 <br/>

https://github.com/langchain-ai/langchain/issues/7634

- DB 업데이트에 걸린 시간: 0초

![2](img/2.GPT4ALL.png)

***

### 3. TensorflowHub

- !pip install tensorflow_text
- from langchain.embeddings import TensorflowHubEmbeddings
- embeddings = TensorflowHubEmbeddings()

에러 <br/>

InvalidDimensionException: Embedding dimension 512 does not match collection dimensionality 1024

- DB 업데이트에 걸린 시간: 5초

![3](img/3.TensorflowHub.png)

***

### 4. *BGE on Hugging Face

- from langchain.embeddings import HuggingFaceBgeEmbeddings
- embeddings = HuggingFaceBgeEmbeddings()
- DB 업데이트에 걸린 시간: 9분

![4](img/4.BGE.png)

***

## 비교

**시간:** 

<br/>2. GPT4All(0초) > 3. TensorflowHub(5초) > 0. HuggingFaceEmbeddings(1분) > 1. intfloat/multilingual-e5-large(4분) > 4. BGE on Hugging Face(9분)

<br/>
<br/>

**성능(개인적인 생각):** 

<br/>1. intfloat/multilingual-e5-large > 3. TensorflowHub > 2. GPT4All > 0. HuggingFaceEmbeddings > 4. BGE on Hugging Face
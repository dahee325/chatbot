import requests
from bs4 import BeautifulSoup # HTML을 파이썬이 보기 좋게 만들어줌
from openai import OpenAI

from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 키워드 기반 챗봇
def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'
    res = requests.get(KOSPI_URL) # HTML가져오기

    selector = '#KOSPI_now'
    soup = BeautifulSoup(res.text, 'html.parser')
    kospi = soup.select_one(selector) # 수많은 html 중에서 하나만 골라줘

    return kospi.text

# chatGPT 기반 챗봇
def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': '너는 사용자와 대화하는 챗봇이야. 항상 예의있게 존댓말로 대답해줘.'},
            {'role': 'user', 'content': user_input},
        ]
    )
    return completion.choices[0].message.content


def langchain(user_input):
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = InMemoryVectorStore(embeddings)

    # 1. load document => 데이터 불러오기
    loader = WebBaseLoader(
        web_paths=(
            'https://n.news.naver.com/mnews/article/081/0003524537',
        )
    )
    docs = loader.load()

    # 2. split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    ) # Recursive : 교집합을 만들면서 자르는 방식
    all_splits = text_splitter.split_documents(docs)

    # 3. stre
    _ = vector_store.add_documents(documents=all_splits) # 안쓰이는 변수의 이름을 _로 설정함

    # 4. retrieve # 가지고있는 데이터 검색하기
    prompt = hub.pull('rlm/rag-prompt')
    retrieved_docs = vector_store.similarity_search(user_input) # 유사도 검색
    docs_content = '\n\n'.join(doc.page_content for doc in retrieved_docs) # 줄바꿈으로 연결
    prompt = prompt.invoke({'question': user_input, 'context': docs_content}) # 질문하기
    answer = llm.invoke(prompt).content

    return answer
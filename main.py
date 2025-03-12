# fastapi : 서버를 만들기 => 127.0.0.1은 내 로컬에서만 돌아가고 있는 서버
# ngrok : 외부에서 접근이 가능하도록 설정
import os
import requests
import random
from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, Request

from utils import kospi, openai, langchain

app = FastAPI()

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
URL = f'http://api.telegram.org/bot{TOKEN}'

@app.post("/") # post : 데이터를 줄테니까 처리해줘
async def read_root(request: Request): # async : 비동기적 함수
    body = await request.json() # 요청된 데이터를 json으로 바꿈, await : 데이터가 처리될 때까지 다음 코드를 실행하지말고 기다려라

    user_id = body['message']['chat']['id']
    text = body['message']['text']

    # 키워드 기반 챗봇
    if text[0] == '/':
        if text == '/lotto':
            numbers = random.sample(range(1, 46), 6) # 리스트
            output = str(sorted(numbers)) # 리스트는 들어가지 못하므로 string으로 바꿈
        elif text == '/kospi':
            output = kospi()
        else:
            output = 'X'
    # chatGPT 기반 챗봇
    else:
        # output = openai(OPENAI_API_KEY, text)
        output = langchain(text)
    requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={output}') # 사용자가 한 말 앵무새처럼 똑같이 응답

    return body


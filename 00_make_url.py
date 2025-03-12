import os
import requests # HTTP를 사용하기 위해 쓰여지는 라이브러리
from dotenv import load_dotenv # .env 파일에 정의된 환경 변수 로드

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'

res = requests.get(URL + '/getUpdates')
res_dict = res.json() # 딕셔너리로 만들기

user_id = res_dict['result'][1]['message']['from']['id']
text = res_dict['result'][1]['message']['text']
# print(user_id, text)

requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={text}') # 주소 실행

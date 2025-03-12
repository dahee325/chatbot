import requests
from bs4 import BeautifulSoup # HTML을 파이썬이 보기 좋게 만들어줌

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'
    res = requests.get(KOSPI_URL) # HTML가져오기
    
    selector = '#KOSPI_now'
    soup = BeautifulSoup(res.text, 'html.parser')
    kospi = soup.select_one(selector) # 수많은 html 중에서 하나만 골라줘

    return kospi.text

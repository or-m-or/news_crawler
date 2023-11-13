import requests
from bs4 import BeautifulSoup
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# http get 요청
req = requests.get('https://beomi.github.io/beomi.github.io_old/')

html = req.text           # HTML 소스코드
# header = req.headers      # HTTP Header
# status = req.status_code  # HTTP Status
# is_ok = req.ok            


# BeautifulSoup으로 html소스를 python객체로 변환
# 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시(Python 내장 html.parser 이용)
soup = BeautifulSoup(html, 'html.parser')

# CSS Selector으로 html 요소 찾기
my_titles = soup.select(
    'h3 > a'
)


data = {}

for title in my_titles:
    data[title.text] = title.get('href')


with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)

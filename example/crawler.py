from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import pyperclip
import subprocess
import time
import requests
import random
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import Request, urlopen
import tempfile
import os
from datetime import datetime
import json


def random_delay(min_seconds, max_seconds):
    """ 무작위 지연 시간을 생성 """
    time.sleep(random.uniform(min_seconds, max_seconds))


# 파일에 내용을 저장하는 함수 (폴더 지정 추가)
def save_to_file(scrapdata):
    folder_name = "results"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    current_time = datetime.now().strftime(r"%Y%m%d_%H%M%S")
    file_title = f"{scrapdata['title'].replace(' ', '_').replace('/', '_')}_{current_time}.txt"

    # scrapdata에서 필요한 값 추출
    section = scrapdata.get('section', '없음')  # 값이 없으면 '없음'을 기본값으로 사용
    query = scrapdata.get('query', '없음')
    title = scrapdata.get('title', '없음')
    author = scrapdata.get('author', '없음')
    content = scrapdata.get('content', '없음')

    # 파일에 작성할 문자열 생성
    # file_content = f'section: {section}\nquery: {query}\ntitle: {title}\nauthor: {author}\ncontent: \n{content}'
    file_content = scrapdata['content']

    with open(os.path.join(folder_name, file_title), 'w', encoding='utf-8') as file:
        # file.write(json.dumps(scrapdata, ensure_ascii=False, indent=4)) 
        file.write(file_content)



# nytimes_login, business_crawler 안에서 chrome_driver() 호출하게 변경하기
def chrome_driver():
    """ 뉴욕타임스 로그인을 위한 크롬 드라이버 객체를 생성하는 함수 """

    # # 크롬 브라우저 디버거 모드로 구동 - 삭제 예정
    # subprocess.Popen(
    # r'C:\Program Files\Google\Chrome\Application\chrome.exe ' 
    # r'--remote-debugging-port=9222 '
    # r'--user-data-dir="C:\chrometemp"'
    # ) 
    
    # Chrome options
    options = webdriver.ChromeOptions()   # 크롬 옵션 객체 생성
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" # User-Agent 설정
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('headless')                                      # headless 모드로 실행
    options.add_argument('--incognito')                                   # 크롬 시크릿 모드로 실행 (로그인 기록 삭제..)
    options.add_argument('--disable-gpu')                                 # 크롬 시크릿 모드 실행 중 GPU 기반/보조 렌더링을 비활성화
    options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 기능 비활성화
    options.add_argument('--ignore-certificate-errors')                   # SSL 인증 에러 무시
    options.add_argument('--no-sandbox')                                  # 크롬 샌드박스모드 비활성화

    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 크롬 디버거 모드로 구동 : 디버거 주소 설정 - 삭제 예정
    
    # 드라이버 경로 지정 및 크롬 드라이버 객체 생성
    driverpath = r'C:\Users\thheo\Documents\crawler_test\chromedriver.exe'
    service = Service(driverpath)
    driver = webdriver.Chrome(service=service, options=options)

    # 드라이버의 모든 쿠키 삭제
    driver.delete_all_cookies()

    return driver
    

# 쿠키 때문에 이미 로그인되어 있다면 로그인 안하는 걸로 코드 수정하기
# 로그인 페이지로 바로 들어가서 로그인 시도 하는 방법으로 수정할 것



# 로그인이 되었는지 안되었는지 판별하는 코드 수정 필요
def nytimes_login(driver):
    """ 뉴욕타임스에 로그인을 수행하는 함수 """
    
    driver.get('https://www.nytimes.com/account')
    random_delay(3,5)
    current_url = driver.current_url
    # exit()
    if current_url == 'https://www.nytimes.com/account': # 수정
        print("이미 로그인되어 있습니다.")
        return True
    else:
        try:
            driver.execute_cdp_cmd("Network.enable", {})

            # 하드코딩 됨 -> 수정 필요
            headers = {
                'Accept'      : 'application/json',
                'Content-Type': 'application/json',
                'Origin'      : r'https://myaccount.nytimes.com',
                'Referer'     : r'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fsubscription%2Fonboarding-offer%3FcampaignId%3D7JFJX%26EXIT_URI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F&asset=masthead',
                'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Req-Details' : '[[it:lui]][[kp:off]]'
            }
            driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})

            # 하드코딩 됨 -> 수정 필요
            nytimes_email = 'dev-admin@rbrain.co.kr'
            nytimes_password = 'Fpdlsqhdn2023!'
        
            # pyperclip.copy(nytimes_email)
            driver.find_element(By.NAME,'email').send_keys(nytimes_email) # Keys.CONTROL + 'v'
            random_delay(1, 3)
            driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button').click() 
            random_delay(1, 3)
            time.sleep(1)

            # pyperclip.copy(nytimes_password)
            driver.find_element(By.NAME, 'password').send_keys(nytimes_password) # Keys.CONTROL + 'v'
            random_delay(1, 3)
            driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button').click()
            random_delay(3, 7)
            time.sleep(1)
            
            print(f"로그인 성공")
            return True
        except Exception as e:
            print(f'로그인 중 에러 발생: {e}')
            return False



# 섹션, 쿼리(키워드), 기사 개수를 입력받고, 기사 본문이 있는 링크를 원소로 가지는 리스트 반환 (일단 하나의 섹션만 선택한다 가정)
def nytimes_newslist(driver, section, query, count):
    driver.get(f'https://www.nytimes.com/search?dropmab=false&query={query}&sections={section}%7Cnyt%3A%2F%2Fsection%2F0415b2b0-513a-5e78-80da-21ab770cb753&sort=best')
    random_delay(1, 3)
    articles = []
    news_url_list = []

    # 원하는 개수가 나올때 까지 more button 클릭
    while len(articles) < count: 
        articles = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="search-bodega-result"]')
        if(len(articles) >= count): break
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="search-show-more-button"]').click()
        except:
            print(f'더보기 버튼이 없음 현재 발견된 데이터만 수집, 발견 기사 : {len(articles)}개')
            break

    # 기사 링크 주소 수집
    for article in articles:
        news_url_list.append(article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

        # 현재까지 수집한 결과 개수 확인
        current_count = len(news_url_list)
        print(f'현재까지 수집한 결과 개수: {current_count}')
        
        # count에 도달하면 종료
        if current_count >= count: break

    # 결과 출력
    print(f'{len(news_url_list)}개의 검색 결과를 수집하였습니다.')
    print(news_url_list)
    return news_url_list



def nytimes_getnews(driver, section, query, url):
    scrapData = {}

    try:
        # URL에서 페이지 내용을 가져옴
        driver.get(url)
        random_delay(1, 3)
        html = driver.page_source
        print(html)
        soup = BeautifulSoup(html, 'html.parser')
        
        # parsedUrl = Request(url, headers={'User-Agent' : "Mozilla/5.0"})
        # soup = BeautifulSoup(urlopen(parsedUrl), 'html.parser')
        

        # # 기사 제목 가져오기
        # title = soup.select_one('h1').text.strip()

        # # 기사 내용 가져오기
        # content = ""
        # paragraphs = soup.select('article p')
        # for paragraph in paragraphs:
        #     content += paragraph.text + '\n'

        # # 기사 작성자 가져오기 (작성자 정보가 있는 경우에만)
        # author = soup.select_one('article span a')
        # author = author.text.strip() if author else "작성자 정보 없음"

        # # 결과 출력 또는 반환
        # scrapData = {
        #     'title': title,
        #     'author': author,
        #     'content': content,
        #     'section': section,
        #     'query': query
        # }
        # return scrapData


    except Exception as e:
        print(f'nytimes_getnews()에서 에러 발생: {e}')
        return {}
    



if __name__=="__main__":
    driver = chrome_driver() 
    login_status = nytimes_login(driver) # True or False

    # 로그인이 성공했다면 크롤링 수행
    if login_status:      
        scrapList = []
        section = 'business'
        query = 'r200'
        crawling_num = 3

        news_url_list = nytimes_newslist(driver, section, query, crawling_num)
        for news_url in news_url_list:
            scrapdata = nytimes_getnews(driver, section, query, news_url)
            scrapList.append(scrapdata)
            save_to_file(scrapdata)
            


        print("scrapList : \n", scrapList)
    else:
        print("로그인 실패로 인해 크롤링을 수행하지 않습니다.")

    driver.quit()

    
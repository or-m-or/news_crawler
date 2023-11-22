import os
import json
import time
from datetime import datetime
import random
import subprocess
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import hashlib
from crawler.news_summary import news_summarizer

CHROMEDRIVER_PATH = r'C:\Users\thheo\Documents\news_crawler\chromedriver.exe'


def random_delay(min_seconds, max_seconds):
    """ 무작위 지연 시간을 생성 """
    time.sleep(random.uniform(min_seconds, max_seconds))


def save_to_text_file(scrapdata):
    """" 크롤링 한 뉴스기사 .txt 파일로 저장 """
    # results 폴더 없으면 생성
    documents_folder = os.path.expanduser("~/documents/news_crawler/documents")
    folder_name = os.path.join(documents_folder, "crawling_results")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 크롤링한 목록 초기화
    news_section = scrapdata.get('section')
    news_query = scrapdata.get('query')
    news_title = scrapdata.get('title', 'No title')
    news_subtitle = scrapdata.get('subtitle', 'No subtitle')
    news_author = scrapdata.get('author', 'No author')
    news_date = scrapdata.get('date', 'No date')
    news_content = scrapdata.get('content', 'No content')


    # 저장할 파일의 이름 생성 (파일명:섹션_쿼리_순번.txt)
    current_time = datetime.now().strftime(r"%m%d_%H%M%S") # 날짜 생성
    file_title = f"{news_section}_{news_query}_{current_time}.txt"
    # hashed_file_name = hashlib.md5(file_title.encode()).hexdigest()

    # 크롤링한 데이터 저장
    # with open(os.path.join(folder_name, f"{hashed_file_name}"), 'w', encoding='utf-8') as file:
    with open(os.path.join(folder_name, file_title), 'w', encoding='utf-8') as file:
        file.write(f"title: {news_title}\n")
        file.write(f"subtitle: {news_subtitle}\n")
        file.write(f"author: {news_author}\n")
        file.write(f"date: {news_date}\n")
        file.write(f"content:\n{news_content}\n")


# nytimes_login, business_crawler 안에서 chrome_driver() 호출하게 변경하기
def chrome_driver():
    """ 크롬 드라이버 객체를 생성하는 함수 """

    # # 크롬 브라우저 디버거 모드로 구동
    subprocess.Popen(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe ' 
        r'--remote-debugging-port=9222 '
        r'--user-data-dir="C:\chrometemp"'
    ) 
    
    # Chrome options
    options = webdriver.ChromeOptions()
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" 
    # options.add_argument(f'user-agent={user_agent}')                      # User-Agent 설정
    # options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 기능 비활성화
    # options.add_argument('--ignore-certificate-errors')                   # SSL 인증 에러 무시
    # options.add_argument('--no-sandbox')                                  # 크롬 샌드박스모드 비활성화
    # options.add_argument('headless')                                      # headless 모드로 실행
    # options.add_argument('--incognito')                                   # 크롬 시크릿 모드로 실행
    # options.add_argument('--disable-gpu')                                 # 크롬 시크릿 모드 실행 중 GPU 기반/보조 렌더링을 비활성화
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 크롬 디버거 모드로 구동 : 디버거 주소 설정


    # 드라이버 경로 지정 및 크롬 드라이버 객체 생성
    # driverpath = os.getenv(CHROMEDRIVER_PATH, chromedriver_autoinstaller.install()) # 드라이버 설치
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
    driver.execute_cdp_cmd("Network.enable", {})


    # http 표준 헤더 변경
    headers = {
        # 'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # 'Accept-Encoding' : 'gzip, deflate, br',
        # 'Accept'      : 'application/json',
        # 'Origin'      : r'https://myaccount.nytimes.com',
        'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', # 없으면 캡챠
        'Content-Type': 'application/json', # 없으면 캡챠
        'Referer'     : r'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fsubscription%2Fonboarding-offer%3FcampaignId%3D7JFJX%26EXIT_URI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F&asset=masthead',
    }
    

    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})
    return driver
    


def nytimes_login(driver):
    """ 뉴욕타임스에 로그인을 수행하는 함수 """

    NYTIMES_EMAIL = os.environ['NYTIMES_EMAIL']
    NYTIMES_PASSWORD = os.environ['NYTIMES_PASSWORD']
    
    try:
        driver.get('https://www.nytimes.com/account')
        random_delay(1, 3)  # 로그인 되어 있지 않다면 위 링크로 접속 시 로그인 페이지로 리다이렉트 됨.

        if driver.current_url == 'https://www.nytimes.com/account':
            print("이미 로그인되어 있습니다.")
            return True
        else:
            driver.get(f'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=acct&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Faccount')
            driver.find_element(By.NAME,'email').send_keys(NYTIMES_EMAIL)
            driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button').click() 
            random_delay(1, 3)

            driver.find_element(By.NAME, 'password').send_keys(NYTIMES_PASSWORD)
            driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button').click()
            random_delay(1, 3)
            
            print(f"로그인 성공")
            return True
    except Exception as e:
        print(f'로그인 중 에러 발생: {e}')
        return False



# 섹션, 쿼리(키워드), 기사 개수를 입력받고, 기사 본문이 있는 링크를 원소로 가지는 리스트 반환 (일단 하나의 섹션만 선택한다 가정)
def nytimes_newslist(driver, section, query, count):
    articles = []
    news_url_list = []
    count = int(count)

    driver.get(f'https://www.nytimes.com/search?dropmab=false&query={query}&sections={section}%7Cnyt%3A%2F%2Fsection%2F0415b2b0-513a-5e78-80da-21ab770cb753&sort=best')
    random_delay(1, 3)

    
    if count == 0:
        count = float('inf')

    # 원하는 개수가 나올때 까지 more button 클릭
    while len(articles) < count: 
        # articles = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="search-bodega-result"]')
        current_articles = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="search-bodega-result"]')
        articles.extend(current_articles[len(articles):])

        if count != float('inf') and len(articles) >= count:
            break
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
    print("url list : \n",news_url_list)
    return news_url_list



def nytimes_getnews(driver, section, query, url):
    scrapData = {}

    try:
    # url 접속하여 html 소스 가져오기
        driver.get(url)
        random_delay(1, 3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 기사 제목 가져오기
        title = soup.select_one('h1').text.strip()

        # 기사 내용 가져오기
        content = ""
        paragraphs = soup.select('article section p')

        for paragraph in paragraphs:
            text = paragraph.text

            # 텍스트에 'Advertisement' 단어가 포함되어 있으면 그 부분을 제외하고 추가
            if 'Advertisement' in text:
                text = text.replace('Advertisement', '')
            content += text + '\n'

        # 기사 소제목 가져오기
        # subtitle = soup.select('article p')
        # subtitle = subtitles[0].get_text()
        # subtitle = subtitle.text.strip() if subtitle else "소제목 정보 없음"
        subtitle = ''

        # 기사 작성자 가져오기, 못 가져오는 경우 있음.
        author = soup.select_one('article span a')
        author = author.text.strip() if author else "No author"

        # 기사 작성 날짜 가져오기
        date = soup.select_one('article time')
        date = date.text.strip() if date else "No date"

        # 결과 출력 또는 반환
        scrapData = {
            'doc_id'  : '',
            'section' : section,
            'query'   : query, 
            'title'   : title,
            'subtitle': subtitle,
            'author'  : author,
            'date'    : date,
            'summary' : '',
            'content' : content,
        }

        # print("title : \n", title)
        # print("sub title : \n", subtitle)
        # print("author : \n", author) # 안 나옴
        # print("date : \n",date) # 가끔 다른 값 나옴 수정 필
        # print("content : \n", content) # 밑에 쓸대없는 단어 추가 됨
        # exit()
        return scrapData
    
    except Exception as e:
        print(f'nytimes_getnews()에서 에러 발생: {e}')
        return {}
    

# 함수명 변경 필요 (패킹 전 병합 중)
def crawling(news_section, news_query, news_count):
    start_time = time.time()
    driver = chrome_driver()
    login_status = nytimes_login(driver) # 로그인 상태 반환

    scraplist = []
    # 로그인에 성공했다면 크롤링 수행
    if login_status:                      
        news_url_list = nytimes_newslist(driver, news_section, news_query, news_count)
        for index, news_url in enumerate(news_url_list):
            print(f'크롤링 수행 중 ...{index+1}/{len(news_url_list)}')
            scrapdata = nytimes_getnews(driver, news_section, news_query, news_url) # dic
            # save_to_text_file(scrapdata) # 크롤링한 파일을 별도로 저장하는 함수
            scraplist.append(scrapdata) # 크롤링한 데이터 저장
    else:
        print("로그인에 실패하였습니다.")

    driver.quit()
    end_time = time.time()  # 종료 시간 기록
    total_time = end_time - start_time  # 총 실행 시간 계산
    print(f"nytimes_crawler 실행 시간: {total_time}초")
    return scraplist


# if __name__=="__main__":
#     news_section = 'Business'
#     news_query = 'r200'
#     news_count = '0'
#     crawling(news_section, news_query, news_count)

    
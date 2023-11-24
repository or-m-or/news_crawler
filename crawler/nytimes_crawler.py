import os
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
from crawler.config import config


def random_delay(min_seconds, max_seconds):
    """ 무작위 지연 시간을 생성 """
    time.sleep(random.uniform(min_seconds, max_seconds))


def chrome_driver(config=config):
    """ 크롬 드라이버 객체를 생성하는 함수 """

    # 크롬 브라우저 디버깅 모드로 구동
    subprocess.Popen(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe ' 
        r'--remote-debugging-port=9222 '
        r'--user-data-dir="C:\chrometemp"'
    ) 
    
    # Chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 크롬 디버거 모드로 구동 : 디버거 주소 설정
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" 
    # options.add_argument(f'user-agent={user_agent}')                      # User-Agent 설정
    # options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 기능 비활성화
    # options.add_argument('--ignore-certificate-errors')                   # SSL 인증 에러 무시
    # options.add_argument('--no-sandbox')                                  # 크롬 샌드박스모드 비활성화
    # options.add_argument('headless')                                      # headless 모드로 실행
    # options.add_argument('--incognito')                                   # 크롬 시크릿 모드로 실행
    # options.add_argument('--disable-gpu')                                 # 크롬 시크릿 모드 실행 중 GPU 기반/보조 렌더링을 비활성화    


    # 드라이버 경로 지정 및 크롬 드라이버 객체 생성
    # driverpath = os.getenv(CHROMEDRIVER_PATH, chromedriver_autoinstaller.install()) # 드라이버 설치
    service = Service(config['path']['chromedriver'])
    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
    driver.execute_cdp_cmd("Network.enable", {})


    # http 표준 헤더 변경
    headers = {
        'Accept-Language' : config['nytimes_header']['Accept-Language'],
        'Content-Type'    : config['nytimes_header']['Content-Type'],
        'Referer'         : config['nytimes_header']['Refer'],
    }
    
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})
    return driver
    

def nytimes_login(driver, config=config):
    """ 뉴욕타임스에 로그인을 수행하는 함수 """

    # NYTIMES_EMAIL    = os.environ['NYTIMES_EMAIL']
    # NYTIMES_PASSWORD = os.environ['NYTIMES_PASSWORD']
    NYTIMES_EMAIL    = config['nytimes']['login_email']
    NYTIMES_PASSWORD = config['nytimes']['login_password']

    try:
        driver.get(config['nytimes']['account_url'])
        random_delay(1, 2)  # 로그인 되어 있지 않다면 위 링크로 접속 시 로그인 페이지로 리다이렉트 됨.

        if driver.current_url == config['nytimes']['account_url']:
            print("이미 로그인되어 있습니다.")
            return True
        else:
            driver.get(config['nytimes']['login_url'])
            driver.find_element(By.NAME,'email').send_keys(NYTIMES_EMAIL)
            driver.find_element(By.XPATH, config['nytimes']['login_email_input']).click() 
            random_delay(1, 2) #3

            driver.find_element(By.NAME, 'password').send_keys(NYTIMES_PASSWORD)
            driver.find_element(By.XPATH, config['nytimes']['login_password_input']).click()            
            print(f"로그인 성공")
            return True
    
    except Exception as e:
        print(f'로그인 중 에러 발생: {e}')
        return False


# 섹션, 쿼리(키워드), 기사 개수를 입력받고, 기사 본문이 있는 링크를 원소로 가지는 리스트 반환 (일단 하나의 섹션만 선택한다 가정)
def nytimes_newslist(driver, section, query, count, config=config) -> list:
    """ 크롤링 가능한 기사의 url 수집하는 함수 """

    articles = []
    news_url_list = []
    count = int(count)

    driver.get(f'https://www.nytimes.com/search?dropmab=false&query={query}&sections={section}%7Cnyt%3A%2F%2Fsection%2F0415b2b0-513a-5e78-80da-21ab770cb753&sort=best')
    random_delay(1, 2)

    if count == 0:
        count = float('inf')

    # 원하는 개수가 나올때 까지 more button 클릭
    while len(articles) < count: 
        current_articles = driver.find_elements(By.CSS_SELECTOR, config['nytimes']['article_css'])
        articles.extend(current_articles[len(articles):])

        if count != float('inf') and len(articles) >= count:
            break
        try:
            driver.find_element(By.CSS_SELECTOR, config['nytimes']['article_plus_button']).click()
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


def nytimes_getnews(driver, section, query, url) -> dict:
    """ url list에 포함된 기사 url에 접속하여 크롤링 수행 """

    scrapData = {}

    try:
    # url 접속하여 html 소스 가져오기
        driver.get(url)
        random_delay(1, 2)
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
        # 'subtitle': subtitle,
        scrapData = {
            'doc_id'  : f'{section}_{query}_{title}',
            'section' : section,
            'query'   : query,
            'title'   : title,
            'author'  : author,
            'date'    : date,
            'content' : content,
            'summary' : '',
        }

        return scrapData
    
    except Exception as e:
        print(f'nytimes_getnews()에서 에러 발생: {e}')
        return {}
    


def crawling(news_section, news_query, news_count):
    start_time = time.time()
    driver = chrome_driver()
    login_status = nytimes_login(driver) # 로그인 상태 반환
    
    # 로그인에 성공했다면 크롤링 수행
    news_docs = []
    if login_status:                      
        news_url_list = nytimes_newslist(driver, news_section, news_query, news_count)
        for index, news_url in enumerate(news_url_list):
            print(f'크롤링 수행 중 ...{index+1}/{len(news_url_list)}')
            scrapdata = nytimes_getnews(driver, news_section, news_query, news_url) # dic
            news_docs.append(scrapdata)
    else:
        print("로그인에 실패하였습니다.")

    driver.quit()
    end_time = time.time()  # 종료 시간 기록
    total_time = end_time - start_time  # 총 실행 시간 계산
    print(f"nytimes_crawler 실행 시간: {total_time}초")
    return news_docs



# def save_to_text_file(scrapdata):
#     """" 크롤링 한 뉴스기사를 .txt 파일로 저장하는 함수 """
#     # results 폴더 없으면 생성
#     documents_folder = os.path.expanduser("~/documents/news_crawler/documents")
#     folder_name = os.path.join(documents_folder, "crawling_results")
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)

#     # 크롤링한 목록 초기화
#     news_section = scrapdata.get('section')
#     news_query = scrapdata.get('query')
#     news_title = scrapdata.get('title', 'No title')
#     news_subtitle = scrapdata.get('subtitle', 'No subtitle')
#     news_author = scrapdata.get('author', 'No author')
#     news_date = scrapdata.get('date', 'No date')
#     news_content = scrapdata.get('content', 'No content')


#     # 저장할 파일의 이름 생성 (파일명:섹션_쿼리_순번.txt)
#     current_time = datetime.now().strftime(r"%m%d_%H%M%S") # 날짜 생성
#     file_title = f"{news_section}_{news_query}_{current_time}.txt"
#     # hashed_file_name = hashlib.md5(file_title.encode()).hexdigest()

#     # 크롤링한 데이터 저장
#     # with open(os.path.join(folder_name, f"{hashed_file_name}"), 'w', encoding='utf-8') as file:
#     with open(os.path.join(folder_name, file_title), 'w', encoding='utf-8') as file:
#         file.write(f"title: {news_title}\n")
#         file.write(f"subtitle: {news_subtitle}\n")
#         file.write(f"author: {news_author}\n")
#         file.write(f"date: {news_date}\n")
#         file.write(f"content:\n{news_content}\n")
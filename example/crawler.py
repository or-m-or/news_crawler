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




def chrome_driver():
    # 크롬 브라우저 디버거 모드로 구동
    subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe ' 
    r'--remote-debugging-port=9222 '
    r'--user-data-dir="C:\chrometemp"'
    ) 
    

    # Chrome options
    chrome_options = webdriver.ChromeOptions()   # 크롬 옵션 객체 생성


    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" # User-Agent 설정
    chrome_options.add_argument(f'user-agent={user_agent}')
    # chrome_options.add_argument('--headless')      # 화면 출력 X
    # chrome_options.add_argument("disable-gpu")   # 가속 사용 x
    # chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 기능 비활성화 - :authority: 수정
    chrome_options.add_argument('--ignore-certificate-errors')                   # SSL 인증 에러 무시

    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 크롬 디버거 모드로 구동 : 디버거 주소 설정
    

    # 드라이버 설정 및 실행
    chromedriver_path = r'C:\Users\thheo\Documents\crawler_test\chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("driver: ",driver)
    nytimes_login(driver)



def random_delay(min_seconds, max_seconds):
    """ 무작위 지연 시간을 생성하는 함수 """
    time.sleep(random.uniform(min_seconds, max_seconds))



def nytimes_login(driver):

    driver.execute_cdp_cmd("Network.enable", {})

    headers = {
        'Accept'      : 'application/json',
        'Content-Type': 'application/json',
        'Origin'      : r'https://myaccount.nytimes.com',
        'Referer'     : r'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fsubscription%2Fonboarding-offer%3FcampaignId%3D7JFJX%26EXIT_URI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F&asset=masthead',
        'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Req-Details' : '[[it:lui]][[kp:off]]'
    }
    """
        ':authority'  : 'myaccount.nytimes.com', # ==Host
        ':path'       : '/svc/lire_ui/login',
        
        # 메타 데이터
        'Sec-Ch-Device-Memory: 8'
        'Sec-Ch-Ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
        'Sec-Ch-Ua-Arch: "x86"'
        'Sec-Ch-Ua-Full-Version-List: "Google Chrome";v="119.0.6045.124", "Chromium";v="119.0.6045.124", "Not?A_Brand";v="24.0.0.0"'
        'Sec-Ch-Ua-Mobile: ?0'
        'Sec-Ch-Ua-Model: ""'
        'Sec-Ch-Ua-Platform: "Windows"'
        'Sec-Fetch-Dest: empty'
        'Sec-Fetch-Mode: cors'
        'Sec-Fetch-Site: same-origin'
    """
    # 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    # X-Pageview-Id:
    # 'Host'        : 'myaccount.nytimes.com',

    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})

    # 로그인 페이지 접속
    driver.get('https://www.nytimes.com')
    driver.find_element(By.CSS_SELECTOR, '#app > div:nth-child(4) > div.NYTAppHideMasthead.css-1r6wvpq.e1m0pzr40 > header > section.css-9kr9i3.e1m0pzr42 > div.css-12bivf2.e1j3jvdr1 > a.css-1kj7lfb > span').click()
    random_delay(1, 3)
    time.sleep(2)


    nytimes_email = 'dev-admin@rbrain.co.kr'
    nytimes_password = 'Fpdlsqhdn2023!'
    
    pyperclip.copy(nytimes_email)
    driver.find_element(By.NAME,'email').send_keys(Keys.CONTROL + 'v')
    random_delay(1, 3)
    # pyautogui.press('tab')
    # pyautogui.press('enter')
    driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button').click() 
    random_delay(1, 3)
    time.sleep(2)


    pyperclip.copy(nytimes_password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.CONTROL + 'v')
    random_delay(1, 3)  # 사용자 입력 사이의 무작위 지연
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('enter')
    driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button').click()
    random_delay(3, 7)  # 로그인 후 대기
    time.sleep(2)
    print("login success")
    

    # 첫 번제 뉴스 접근 테스트 - success
    driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/div/div[1]/div/section[1]/a/div/div/h3').click()
    random_delay(1, 3) 
    time.sleep(2)


    # 새로 열린 페이지의 HTML을 가져오고 뉴스 내용을 추출
    new_page_html = driver.page_source
    soup = BeautifulSoup(new_page_html, 'html.parser') # soup로 만들기

    title = soup.select('#link-61dd875')
    contents = soup.select('#story > section > div:nth-child(1) > div > p:nth-child(3)')

    print(title[0].text)
    print(contents[0].text)

    
    # driver.implicitly_wait(30)
    time.sleep(5)
    driver.quit()
    


if __name__=="__main__":
    chrome_driver()
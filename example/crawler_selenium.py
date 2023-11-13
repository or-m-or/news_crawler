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


# poetry test, project 자동 생성해주는 명령어 찾아서 추가하기 (키워드 : new)



def search():
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
    # chrome_options.add_argument(f'user-agent={random_user_agent()}')
    # chrome_options.add_argument("app-version = "+ user_agent)
    chrome_options.add_argument('--ignore-certificate-errors')                   # SSL 인증 에러 무시
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 프로그램 인식 방지?
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 크롬 디버거 모드로 구동 : 디버거 주소 설정
    

    # 드라이버 설정 및 실행
    chromedriver_path = r'C:\Users\thheo\Documents\crawler_test\chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    nytimes_login(driver)
    # naver_login(driver)


def search2():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" # User-Agent 설정

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") # 디버깅 모드
    chrome_options.add_argument('--ignore-certificate-errors')                   # SSL 인증 에러 무시
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 프로그램 인식 방지?
    chrome_options.add_argument(f'user-agent={user_agent}')

    chrome_driver = r'C:\Users\thheo\Documents\crawler_test\chromedriver.exe'
    chrome_service = Service(chrome_driver)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    nytimes_login(driver)







def random_delay(min_seconds, max_seconds):
    """ 무작위 지연 시간을 생성하는 함수 """
    time.sleep(random.uniform(min_seconds, max_seconds))

def random_user_agent():
    """ 무작위 사용자 에이전트를 생성하는 함수 """
    platforms = ["Windows", "Linux", "Mac"]
    browsers = ["Chrome", "Firefox", "Safari"]
    versions = ["99", "100", "101"]

    return f"Mozilla/5.0 ({platforms[random.randint(0, 2)]} {browsers[random.randint(0, 2)]} {versions[random.randint(0, 2)]}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"



def nytimes_login(driver):

    # 로그인 페이지 접속
    driver.get('https://www.nytimes.com/international/')
    driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/header/section[1]/div[4]/a[1]/span').click()
    random_delay(1, 3)
    time.sleep(5)


    nytimes_email = 'dev-admin@rbrain.co.kr'
    nytimes_password = 'Fpdlsqhdn2023!'
    
    pyperclip.copy(nytimes_email)
    driver.find_element(By.NAME,'email').send_keys(Keys.CONTROL + 'v')
    random_delay(1, 3)
    pyautogui.press('tab')
    pyautogui.press('enter')
    # driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button').click() 
    random_delay(1, 3)
    time.sleep(5)


    pyperclip.copy(nytimes_password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.CONTROL + 'v')
    random_delay(1, 3)  # 사용자 입력 사이의 무작위 지연
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    # driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button').click()
    random_delay(3, 7)  # 로그인 후 대기
    time.sleep(5)

    # 로그인 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="frmNIDLogin"]/fieldset/input').click() # //*[@id="log.login"]
    driver.implicitly_wait(30)
    time.sleep(10)
    # 여기서 봇 탐지 

    print('login success')



def naver_login(driver):
    driver.get(r'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')  # 네이버
    time.sleep(0.5)
    
    id = 'hth815'
    pw = 'ormor815#'

    pyperclip.copy(id)
    driver.find_element(By.NAME, 'id').send_keys(Keys.CONTROL + 'v')
    time.sleep(0.7)

    pyperclip.copy(pw)
    driver.find_element(By.NAME, 'pw').send_keys(Keys.CONTROL + 'v')
    time.sleep(0.7)

    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    time.sleep(1)

    # driver.find_element(By.NAME, 'id').send_keys('hth815')
    # random_delay(1, 3)
    # driver.find_element(By.NAME, 'pw').send_keys('ormor815#')
    # random_delay(1, 3)

    # driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    # random_delay(3, 7)  # 로그인 후 대기



if __name__=="__main__":
    search()
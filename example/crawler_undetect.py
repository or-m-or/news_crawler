import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
import pyperclip
from selenium.webdriver.common.keys import Keys

options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument('--disable-popup-blocking') # 팝업 차단을 활성화합니다.


# WebDriver 객체 생성
driver = uc.Chrome(options=options, enable_cdp_events=True, incognito=True)

# selenium_stealth 설정
stealth(driver,
        vendor="Google Inc. ",
        platform="Win64",
        webgl_vendor="intel Inc. ",
        renderer= "Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


options.add_argument('--remote-debugging-port=9222')

# 웹사이트 방문
driver.get('https://www.nytimes.com/')
driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/header/section[1]/div[4]/a[1]/span').click()


# 대기 시간 설정 =&gt; 대기 시간을 설정하여, html이 렌더링 되는 시간을 벌어줍니다.
driver.implicitly_wait(2)

# 자바스크립트 코드 실행
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")





try:
    nytimes_email = 'dev-admin@rbrain.co.kr'
    nytimes_password = 'Fpdlsqhdn2023!'
    
    # 이메일 입력
    pyperclip.copy(nytimes_email)
    driver.find_element(By.NAME,'email').send_keys(Keys.CONTROL + 'v')
    driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button').click()
    driver.implicitly_wait(2)
    driver.delete_all_cookies()
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

    # 비밀번호 입력
    pyperclip.copy(nytimes_password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.CONTROL + 'v')
    driver.find_element(By.XPATH, '//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button').click()
    driver.implicitly_wait(2)
    driver.delete_all_cookies()
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")


    # 로그인 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="frmNIDLogin"]/fieldset/input').click() # //*[@id="log.login"]
    driver.implicitly_wait(2)
    driver.delete_all_cookies()
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

except:
    print("차단당함")
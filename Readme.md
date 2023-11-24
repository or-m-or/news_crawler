## News Crawler

본 프로그램은 NewYorkTimes 및 Bloomberg를 대상으로 사용자가 입력한 조건에 부합하는 뉴스 기사를 수집하고, 각 개별 기사를 요약 및 번역하는 과정을 수행합니다.

## 실행 방법

1. 사용 중인 크롬 브라우저 버전에 일치하는 크롬 드라이버 설치 : 
    - [크롬 드라이버 설치 링크](https://chromedriver.chromium.org/downloads)를 클릭하여 사용 중인 크롬 브라우저와 일치하는 버전의 드라이버를 설치합니다.
    - `chromedriver.exe` 파일을 `./news_crawler/chromedriver.exe` 에 저장합니다.
    - 현재 크롤링에 사용되는 크롬 브라우저 및 드라이버 버전은 아래와 같습니다. 
        > **크롬 브라우저 버전** ->  119.0.6045.160(공식 빌드) (64비트)   
        > **크롬 드라이버 버전** ->  119.0.6045.159 (r1204232) win64


2. 가상 환경 생성

    ```shell
    python -m venv .venv
    ```

3. 의존성 설치

    ```shell
    poetry install
    ```

4. News Crawler 실행 <br>
    다음과 같이 터미널에 기입하여 프로그램을 실행합니다. <br>
    ```shell
    python crawler_usage.py <언론사 이름> <뉴스 섹션> <검색할 키워드> <크롤링할 뉴스 개수>
    ```
    - 현재는 언론사 이름 칸에 nytimes만 기입할 수 있습니다. (bloomberg 추가 예정)
    - 뉴스 섹션의 종류는 Any, Arts, Books, Business, New York, Opinion, Sports, Style, U.S., World, politics, Health, Technology, Science 등... 을 기입할 수 있습니다.
    - 뉴스 개수에 0을 기입하였을 경우, 조건에 해당되는 모든 뉴스 기사를 가져옵니다.
    
    

## 참고 사항

1. 현재 본 프로그램에서 크롤링을 수행할 때, 크롬 드라이버는 디버깅 모드로 실행됩니다.

2. 현재 로그인을 수행할 때, Request에 포함되는 HTTP 표준 헤더 값들 중 수정된 속성은 다음과 같습니다. 
    - **Accept-Language**
    - **Content-Type**
    - **Referer**

3. 캡챠가 발생할 수 있는 상황과 해결 가능한 방법
    - 본 프로그램을 대략 10회 이상 재 실행 할 경우 즉, 크롤러로 15회 가량 로그인을 시도할 경우 캡차가 발생할 수 있습니다.
    - 위와 같은 이유로 캡챠가 발생한 경우, 접속 중인 인터넷 ip 주소를 변경하여 해결할 수 있습니다. (모바일 핫스팟에 연결하는 등)
    - 그럼에도 계속 캡챠가 발생하는 경우, 추가로 수정 가능한 헤더 값은 아래와 같으며 `./crawler/config.py` 에 사람이 로그인 했을 때 Request에 포함되는 속성 값이 작성되어 있습니다.
        - **User-Agent**
        - **Accept-Encoding**
        - **Accept**
        - **Origin**

4. 출력 값은 CSV파일로 저장되며 `'뉴스 제목'`, `'기사 작성자'`, `'기사 작성일자'`, `'요약 및 번역 결과'`, `'뉴스 원문'` 와 같은 값이 저장됩니다.
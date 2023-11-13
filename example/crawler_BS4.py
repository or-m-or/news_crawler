import requests
from bs4 import BeautifulSoup as bs


def BeautifulSoup_login():
    # 로그인 정보
    LOGIN_INFO = {
        'userId'       : 'ormor',   # js코드에서 HTML form field 의 아이디가 작성되는 부분의 key
        'userPassword' : 'ormor815'
    }

    with requests.Session() as s:

        first_page = s.get('https://www.clien.net/service')
        html = first_page.text
        soup = bs(html, 'html.parser')


        # csrf : CSRF는 사용자의 요청이 악의적이거나 제 3자에 의해 변조된(해킹된) 요청이 아닌지 확인해주는 보안 도구
        # csrf가 없는 폼 전송은 로그인 안됨.
        csrf = soup.find('input', {'name': '_csrf'}) # input 태그 중 name = _csrf 찾기
        print(csrf['value'])


        # LOGIN_INFO에 csrf값 넣기
        LOGIN_INFO = {**LOGIN_INFO, **{'_csrf': csrf['value']}} # dict 2개 unpacking
        print(LOGIN_INFO)


        # 로그인
        login_req = s.post('https://www.clien.net/service', data=LOGIN_INFO)
        print(login_req.status_code)


        if login_req.status_code == 200:
            post_one = s.get('https://www.clien.net/service/board/rule/10707403', data=LOGIN_INFO)
            soup = bs(post_one.text, 'html.parser')

            # 공지글 제목 CSS selector 선택
            title = soup.select('#div_content > div.post_title.symph_row > h3 > span')
            # 공지글 내용 CSS selector 선택
            contents = soup.select('#div_content > div.post_view > div.post_content > article > div')

            print(title[0].text)    # 글 제목 가져오기
            print(contents[0].text) # 글 내용 가져오기


        # # http get 요청 : rquests 대신 session()객체 사용
        # req = s.get('https://www.clien.net/service/')

        # html = req.text           # html 소스
        # header = req.headers      # http header
        # status = req.status_code  # http status
        # is_ok = req.ok



if __name__=="__main__":
    BeautifulSoup_login()
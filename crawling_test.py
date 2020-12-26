from urllib.request import urlopen   # urlopen 함수는 웹에서 얻은 데이터에 대한 객체를 반환해줍니다
from urllib.parse import quote_plus  # 문자를 아스키코드로 변환하여 url에 넣기 위해
from bs4 import BeautifulSoup   # beautifulsoup 사용
from selenium import webdriver  # 웹드라이버 사용
from selenium.webdriver.common.keys import Keys  # 웹에서 값을 입력해야할 때 사용
import time
import os  # 이미지를 저장할 폴더를 생성할때 필요


# CERTIFICATE_VERIFY_FAILED 오류 해결
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 아이디, 패스워드 입력받기
# 인스타그램에서 검색을 하려면 반드시 로그인을 해야 사용가능하게끔 바꼈습니다..
# 자동화를 위해 코드에 id와 pw를 넣으면 좋지만 보안상 input을 이용해 입력을 받아 구현하였습니다.

id = input('instagram 아이디 및 계정 입력 : ')
pw = input('instagram 패스워드 입력 : ')

# 필요한 url설정
baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input("검색할 태그 입력 : ")
scroll_cnt = int(input("스크롤 횟수 : "))

url = baseUrl + quote_plus(plusUrl)  # quote_plus를 이용하여 아스키코드로 변환

# 이미지를 저장할 img 폴더 생성 (폴더가 없을때만 생성)
if not os.path.exists('./img'):
    os.mkdir('./img')

# 브라우저 실행 및 인스타그램 로그인 화면 이동
driver = webdriver.Chrome()
driver.get('https://www.instagram.com/accounts/login/')

time.sleep(2)  # 웹드라이버가 웹 페이지를 로딩하는데 걸리는 시간을 기다려주기 위해 (>> Selenium의 단점..)

# 로그인
id_input = driver.find_element_by_css_selector(
    '#loginForm > div > div:nth-child(1) > div > label > input')
pw_input = driver.find_element_by_css_selector(
    '#loginForm > div > div:nth-child(2) > div > label > input')

id_input.send_keys(id)
pw_input.send_keys(pw)
pw_input.submit()

time.sleep(4)


# 로그인 후 뜨는 팝업창 해결
save_late_button1 = driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div/div/div/button')
save_late_button1.click()

driver.implicitly_wait(3)  # 모든 요소가 다 받아질때까지 최대 3초 기다림

save_late_button2 = driver.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]')
save_late_button2.click()

# 검색 페이지로 이동
driver.get(url)
time.sleep(1)


# 스크롤 반복
for i in range(scroll_cnt):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

time.sleep(3)


# 드라이버로 페이지 소스를 가져와서 html 변수에 저장
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


# 검색된 모든 인스타 게시물 선택(아래 selector를 가지고 있는 것을 불러와서 저장)
posts = soup.select('.v1Nh3.kIKUG._bz0w')  # 클래스가 여러개인 경우는 공백을 없애고 .으로 이어주기
# posts 변수에는 .v1Nh3.kIKUG._bz0w 이 selector를 가지고 있는 모든 태그들이 들어감.


# 각 게시물의 링크와 이미지 url가져오기
for index, post in enumerate(posts):
    print('https://www.instagram.com/' + post.a['href'])
    imgUrl = post.select_one('.KL4Bh').img['src']
    with urlopen(imgUrl) as f:  # imgUrl을 열어서 저장

        # 저장한 imgUrl을 다시 열어서 이미지 파일로 파일 이름을 지정해서 저장
        with open('./img/' + plusUrl + str(index) + '.jpg', 'wb') as h:
            # wb는 쓰기모드 + 바이너리모드. 이미지이기때문에 b모드를 써줘야한다.
            image = f.read()  # f를 읽어와서 img라는 변수 안에 저장
            h.write(image)   # 가져온 이미지를 해당 경로에 지정된 이름으로 저장

    print(imgUrl)
    print()


# 코드 실행 잠시 멈춤
time.sleep(2)

# 드라이버 종료
driver.quit()

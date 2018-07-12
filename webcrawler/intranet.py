from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from bs4 import BeautifulSoup

def parsed_subject(id, pw):
    
    # webdriver 정보
    driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver")
    driver.implicitly_wait(3)

    # 웹정보서비스 로그인 URL
    driver.get("http://intra.wku.ac.kr/SWupis/V005/login.jsp") 

    # 로그인을 위한 id, pw 정보
    driver.find_element_by_name('userid').send_keys(id)
    driver.find_element_by_name('passwd').send_keys(pw)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath(
        "//*[@id = 'f_login']/fieldset/dl/dd[3]/input").click()

    # 접속 후 Alert 창 확인
    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
        alert = driver.switch_to_alert()
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")


    # 전체 성적 리스트 주소
    driver.get(
        "http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Score/scoreAll.jsp?sm=3")

    # 페이지 로드 대기
    driver.implicitly_wait(5)

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    except selenium.common.exceptions.UnexpectedAlertPresentException:
        pass

    select_year = soup.select(
        'body > table > tbody > tr > td:nth-of-type(6) > a')

    year_list = []

    for item in select_year:
        year_list.append(item)

    # 데이터를 담을 전체 리스트
    information = []
    subject = {}
    sum_of_grade_point = 0

    for x in year_list:
        driver.get("http://intra.wku.ac.kr" + x['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 이수구분
        subject_kind = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(1)')
        # 과목명
        subject_list = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(3)')
        # 학점
        subject_grade_point = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(4)')
        # 점수
        subject_grade = soup.select(
            'body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(6)')

        for kind, title, point, grade in zip(subject_kind, subject_list, subject_grade_point, subject_grade):
            subject[title.text] = [kind.text, point.text, grade.text]
            sum_of_grade_point += float(point.text)


    information.append(subject)
    information.append({'sum_of_grade_point' : sum_of_grade_point})

    driver.close()

    return information

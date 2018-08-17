from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from bs4 import BeautifulSoup
import time
from datetime import datetime
from pyvirtualdisplay import Display
def parser(id, pw):

    start = datetime.now()

    # display = Display(visible=0, size=(800, 600))
    # display.start()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # webdriver 정보
    driver = webdriver.Chrome("/Users/marine/Downloads/chromedriver", chrome_options=options)
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
    # driver.implicitly_wait(3)

    # 웹정보서비스 로그인 URL
    driver.get("http://intra.wku.ac.kr/SWupis/V005/login.jsp")

    # 로그인을 위한 id, pw 정보
    driver.find_element_by_id('userid').send_keys(id)
    # driver.find_element_by_name('userid').send_keys(id)
    driver.find_element_by_id('passwd').send_keys(pw)
    # driver.find_element_by_name('passwd').send_keys(pw)

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

    # 로그인 실패
    if driver.current_url[:54] == "http://intra.wku.ac.kr/SWupis/V005/login.jsp?error_msg":
        return "login_fail"

    print('After Login: ', datetime.now() - start)
    ### 사용자 정보 크롤링
    ### 이름, 학번, 이미지, 학년, 소속, 이수학기, 전공

    driver.get('http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Resume/resume.jsp?sm=3')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    user_name = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(4)')
    user_number = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2)')
    user_image = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(1) > table > tbody > tr > td > img')
    user_grade = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2)')
    user_college = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2)')
    user_completed_semester = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4)')
    user_major = soup.select('body > table:nth-of-type(1) > tbody > tr > td:nth-of-type(3) > form > table > tbody > tr:nth-of-type(4) > td:nth-of-type(4)')

    user_name = user_name[0].text
    user_number = user_number[0].text
    user_image = user_image[0]['src']
    user_grade = user_grade[0].text
    user_college = user_college[0].text
    user_completed_semester = user_completed_semester[0].text
    user_major = user_major[0].text

    # 사용자 정보 : 이름, 학번, 이미지경로, 학년, 단과대학명, 이수학기, 전공
    user_info = [user_name, user_number, user_image, user_grade, user_college, user_completed_semester, user_major]

    print('After User info: ', datetime.now() - start)
    ### 장학 이력 정보 크롤링
    ### 년도, 학기, 장학명, 장학입학금, 장학수업료, 계

    driver.get('http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Search/scholarResume.jsp?sm=3')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    scholar_ship = []

    year = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(1)')
    semester = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(2)')
    scholar_name = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(3)')
    scholar_money1 = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(4)')
    scholar_money2 = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(5)')
    scholar_total = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(6)')

    for t_year, t_semester, t_scholar_name, t_scholar_money1, t_scholar_money2, t_scholar_total in zip(year, semester, scholar_name, scholar_money1, scholar_money2, scholar_total):
        scholar_ship.append([
            t_year.text,
            t_semester.text,
            t_scholar_name.text,
            t_scholar_money1.text,
            t_scholar_money2.text,
            t_scholar_total.text
        ])

    print('After scholar_ship: ', datetime.now() - start)

    ### W - POINT 크롤링
    ### 도덕성, 창의성, 소통력, 실천력, 포인트 합계
    ### 사업참여 내역

    # driver.get('http://intra.wku.ac.kr/SWupis/V005/CommonServ/entire/job/extra_wpoint.jsp')
    # time.sleep(1)

    # html = driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')
    # wpoint = []

    # # ### 인정 포인트, 현재 포인트
    # accept_table = soup.select('table:nth-of-type(3) > tbody > tr:nth-of-type(2) > th')
    # accept_point = soup.select('table:nth-of-type(3) > tbody > tr:nth-of-type(3) > td')
    # over_table = soup.select('table:nth-of-type(3) > tbody > tr:nth-of-type(5) > th')
    # over_point = soup.select('table:nth-of-type(3) > tbody > tr:nth-of-type(6) > td')

    # for t_accept_table, t_accept_point, t_over_table, t_over_point in zip(accept_table, accept_point, over_table, over_point):
    #     wpoint.append([
    #         t_accept_table.text,
    #         t_accept_point.text,
    #         t_over_table.text,
    #         t_over_point.text,
    #     ])

    ### 사업참여 내역

    # detail_wpoint = []

    # industry_name = soup.select('table:nth-of-type(4) > tbody > tr > td:nth-of-type(1) > a > strong')
    # industry_duration = soup.select('table:nth-of-type(4) > tbody > tr > td:nth-of-type(2)')
    # industry_info = soup.select('table:nth-of-type(4) > tbody > tr > td:nth-of-type(3)')
    # industry_accept_point = soup.select('table:nth-of-type(4) > tbody > tr > td:nth-of-type(4)')
    # industry_over_point = soup.select('table:nth-of-type(4) > tbody > tr > td:nth-of-type(5)')
    # industry_accepted = soup.select('table:nth-of-type(4) > tbody > tr > td:nth-of-type(6)')

    # for t_industry_name, t_industry_duration, t_industry_info, t_industry_accept_point, t_industry_over_point, t_industry_accepted in zip(industry_name, industry_duration, industry_info, industry_accept_point, industry_over_point, industry_accepted):
    #     detail_wpoint.append([
    #         t_industry_name.text,
    #         t_industry_duration.text,
    #         t_industry_info.text,
    #         t_industry_accept_point.text,
    #         t_industry_over_point.text,
    #         t_industry_accepted.text,
    #     ])


    # 전체 성적 리스트 주소
    driver.get("http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Score/scoreAll.jsp?sm=3")
    # 페이지 로드 대기
    # driver.implicitly_wait(3)

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    except selenium.common.exceptions.UnexpectedAlertPresentException:
        pass

    # driver.implicitly_wait(3)

    # 각 년도별 성적 리스트 주소 추출
    select_year = soup.select('body > table > tbody > tr > td:nth-of-type(6) > a')

    ## 평균 학점
    ## 년도, 학년, 학기, 평균학점

    average_point_year = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(1)')
    average_point_grade = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(2)')
    average_point_semester = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(3)')
    average_point = soup.select('body > table:nth-of-type(2) > tbody > tr > td:nth-of-type(7)')
    average_point_total = soup.select('body > table:nth-of-type(3) > tbody > tr:nth-of-type(2) > td:nth-of-type(3)')[0].text

    average_point_year = [item for item in average_point_year]
    average_point_grade = [item for item in average_point_grade]
    average_point_semester = [item for item in average_point_semester]
    average_point = [item for item in average_point]
    average_point_info = []

    for year, grade ,semester, point in zip(average_point_year, average_point_grade, average_point_semester, average_point):
        average_point_info.append([year.text, grade.text, semester.text, point.text])


    # 데이터를 담을 전체 리스트
    information = []
    subject = {}
    sum_of_grade_point = 0

    print('After average_point: ', datetime.now() - start)

    ## 전체성적리스트 페이지
    driver.get("http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Score/scoreList.jsp")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    t_data = soup.select("body > table > tbody")

    flag1 = False
    flag2 = False
    y = []
    s = []
    total_point = []
    average_p = []
    sub_info = {}

    t_data[0].select("td") # 단과대학, 전공, 학번, 이름
    for item in t_data[1].select("tr"):
        data = item.select('td')
        data = [x.text for x in data]

        if data and data[0].find("년") != -1:
            year = data[0][0:4]
            semester = data[0][9:10]
        
        if data and data[0].find("취득학점") != -1:
            total_point = data[1]
            average_p = data[2]

        if data and len(data) > 3:
            if data[2] in sub_info:
                sub_info[data[2] + '(' + year + '-' + semester + ')'] = [data[0], data[1], data[3], data[5], year, semester, data[4]]
            else:
                sub_info[data[2]] = [data[0], data[1], data[3], data[5], year, semester, data[4]]
            sum_of_grade_point += float(data[3])

    print('After user grade point: ', datetime.now() - start)

    information.append(sub_info)  # 교과목 정보
    information.append({'sum_of_grade_point' : sum_of_grade_point}) # 전체 이수학점
    information.append(user_info) # 사용자 정보
    information.append(scholar_ship) # 장학금 정보
    # information.append(wpoint) # WPOINT 정보
    # information.append(detail_wpoint) # WPOINT 상세정보
    information.append(average_point_info) # 평균 학점 정보
    information.append(float(average_point_total)) # 전체 평균 학점

    driver.close() # 크롤링 끝
    driver.quit()
    # display.stop()

    finish = datetime.now() - start
    print(finish)

    return information

### 학과별 과목 크롤링 파서

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import os, sys
from pyvirtualdisplay import Display

def subject_parser(id, pw):
    

    # 가상 디스플레이 셋팅
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intra_crawling.settings")
    import django
    django.setup()

    from webcrawler.models import Subject, Major

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver2",  chrome_options=options)
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.get("http://intra.wku.ac.kr/SWupis/V005/login.jsp")


    # 로그인을 위한 id, pw 정보
    driver.find_element_by_name('userid').send_keys(id)
    driver.find_element_by_name('passwd').send_keys(pw)
    time.sleep(1)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath("//*[@id = 'f_login']/fieldset/dl/dd[3]/input").click()
    time.sleep(1)

    # 접속 후 Alert 창 확인
    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
        alert = driver.switch_to_alert()
        alert.accept()
    except TimeoutException:
        pass

    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
        alert = driver.switch_to_alert()
        alert.accept()
    except TimeoutException:
        pass

    # 학과별 교육과정 조회
    driver.get('http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Course/listByDept.jsp?sm=3')

    # year = [str(year) for year in range(2014, 2018)] # 2000년 ~ 2018년
    # grade = [str(grade) for grade in range(1, 5)] # 1 ~ 6학년
    colleage = [1961, 55]
    codeRegiment = {
        '1961' : [1979],
        '55' : [387]
    }
    # colleage = [1541, 1676, 42, 1963, 49, 54, 48, 57, 867, 50, 1962, 1961, 56, 52, 55, 53, 44, 47, 607, 1169, 1232, 1234, 1418, 1420, 1562, 1595, 515, 61]
    # codeRegiment = {
    #     '1541' : [1542, 1543, 1544, 1545, 1621, 1622, 2049], # 경영대학
    #     '1676' : [1678, 1679, 1680, 1893], # 공공정책대학
    #     '42' : [277, 1014, 1773], # 교학대학
    #     '1963' : [1989, 1990, 1991, 1992, 1993, 2034, 2035, 2036, 2037, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2126], # 농식품융합대학
    #     '49' : [314, 315 ,316, 317, 319, 320, 322, 325, 328, 1030, 1312, 1314], # 사범대학
    #     '54' : [374, 805, 1558, 2009, 2010, 2011], # 사회과학대학
    #     '48' : [312, 1446], # 약학대학
    #     '57' : [399, 400, 1315, 1681], # 의과대학
    #     '867' : [873, 876, 878, 879, 880, 881, 882, 1029, 1167, 1440, 1770, 1988, 2044, 2045, 2046, 2047, 2048, 2067], # 인문대학
    #     '50' : [340, 343, 1018, 1186, 1356, 1548, 1549, 1551, 1994, 2116, 2117], # 자연과학대학
    #     '1962' : [1984, 1985, 1986, 1987, 2032, 2033, 2038], # 조형예술디자인대학
    #     '1961' : [1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 2029, 2030, 2031, 2065], # 창의공과대학
    #     '56' : [396, 397], # 치과대학
    #     '52' : [350, 351], # 한의과대학
    #     '55' : [383, 385, 386, 387, 391, 392, 1034, 1132, 1353, 1354, 1417, 1559, 1560], # 공과대학
    #     '53' : [363, 975, 1108, 1151, 1554, 1555, 1556, 1557], # 미술대학
    #     '44' : [294], # 법과대학
    #     '47' : [1591, 1771, 1775, 1776, 1777, 1780, 1782, 1783, 1784], # 생명자원과학대학
    #     '607' : [609, 837, 1146, 1552, 1553], # 생활과학대학
    #     '1169' : [], # 군사학부
    #     '1232' : [], # 경찰행정학부
    #     '1234' : [1235], # 소방행정학부
    #     '1418' : [], # 인문사회자율전공학부(대학)
    #     '1420' : [], # 자연과학자율전공학부(대학)
    #     '1562' : [], # 봉황인재학부(대학)
    #     '1595' : [1596, 1597, 1598, 1599], # 경영대학(야)
    #     '515' : [1532, 1533, 1534, 1535, 1785, 1786, 1787, 1788], # 공과대학(야)
    #     '61' : [437, 438], # 경상대학
    #     }

    for y in range(2014, 2019):
        select_year = Select(driver.find_element_by_name('year'))
        try:
            select_year.select_by_value(str(y))
        except NoSuchElementException:
            select_year = None

        for g in range(1,5):
            select_grade = Select(driver.find_element_by_name('grade'))
            try:
                select_grade.select_by_value(str(g))
            except NoSuchElementException:
                select_grade = None

            for c in colleage:
                select_colleage = Select(driver.find_element_by_name('college'))
                try:
                    select_colleage.select_by_value(str(c))
                except NoSuchElementException:
                    select_colleage = None

                for major_code in codeRegiment[str(c)]:
                    select_codeRegiment = Select(driver.find_element_by_name('codeRegiment'))
                    try:
                        select_codeRegiment.select_by_value(str(major_code))
                    except NoSuchElementException:
                        select_codeRegiment = None
 
                    driver.find_element_by_xpath("/html/body/form/input[1]").click()

                    try:
                        WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
                        alert = driver.switch_to_alert()
                        alert.accept()
                    except TimeoutException:
                        pass
                    
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    grade = soup.find('select', {"name" : "grade"}).find_all('option', {'selected': True})[0].text
                    major_name = soup.find('select', {"name" : "codeRegiment"}).find_all('option', {'selected': True})
                    if major_name:
                        major_name = major_name[0].text
                    
                    print(y, grade, major_name)
                    # print(major_name)

                    year = soup.find('select', {"name" : "year"}).find_all('option', {'selected': True})
                    if year:
                        year = int(year[0].text[:4])
                    
                    subject_semester = soup.select(
                        "body > table > tbody > tr > td:nth-of-type(1)")
                    subject_type = soup.select("body > table > tbody > tr > td:nth-of-type(2)")
                    subject_number = soup.select(
                        "body > table > tbody > tr > td:nth-of-type(3)")
                    subject_name = soup.select(
                        "body > table > tbody > tr > td:nth-of-type(4) > b")
                    subject_point = soup.select(
                        "body > table > tbody > tr > td:nth-of-type(5)")
                    subject_theory = soup.select(
                        "body > table > tbody > tr > td:nth-of-type(6)")
                    subject_training = soup.select(
                        "body > table > tbody > tr > td:nth-of-type(7)")
                    subject_host = soup.select("body > table > tbody > tr > td:nth-of-type(8)")

                    for a, b, c, d, e, f, g, h in zip(subject_semester, subject_type, subject_number, subject_name, subject_point, subject_theory, subject_training, subject_host):
                        # print(year, a.text, b.text, c.text, d.text, e.text, f.text, g.text, h.text)
                        
                        try: 
                            major = Major.objects.get(name=major_name)
                        except Major.DoesNotExist:
                            major = False

                        if not major:
                            if major_name:
                                major = Major(name=major_name, certification=False)
                                major.save()
                        else:
                            if Subject.objects.filter(title=d.text, subject_year=year, subject_grade=grade, subject_semester=int(a.text)):
                                pass
                            else:
                                if not c.text:
                                    subject = Subject(title=d.text, major=major, subject_grade=grade, subject_year=year, subject_semester=int(a.text), subject_type=b.text, subject_point=int(float(e.text)), subject_theory=f.text,
                                        subject_training=g.text, necessary=False, subject_detail_major=h.text).save()
                                else:
                                    subject = Subject(title=d.text, major=major, subject_grade=grade, subject_year=year, subject_semester=int(a.text), subject_type=b.text, subject_number=int(c.text), subject_point=int(float(e.text)), subject_theory=f.text,
                                        subject_training=g.text, necessary=False, subject_detail_major=h.text).save()


    driver.close()
    driver.quit()
    # display.stop()


if __name__=='__main__':
    id = input("인트라넷 id: ")
    pw = input("인트라넷 pw: ")

    subject_parser(id, pw)
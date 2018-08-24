### 영역별 과목 크롤링 파서

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome("/Users/k352ex/Downloads/Chromedriver")
driver.get("http://intra.wku.ac.kr/SWupis/V005/login.jsp")

# 로그인을 위한 id, pw 정보
driver.find_element_by_name('userid').send_keys("")
driver.find_element_by_name('passwd').send_keys("")

# 로그인 버튼 클릭
driver.find_element_by_xpath("//*[@id = 'f_login']/fieldset/dl/dd[3]/input").click()

# 접속 후 Alert 창 확인
try:
    WebDriverWait(driver, 1).until(EC.alert_is_present(), "test")
    alert = driver.switch_to_alert()
    alert.accept()
except TimeoutException:
    pass
    
# 영역별 교육과정 조회
driver.get('http://intra.wku.ac.kr/SWupis/V005/Service/Stud/Course/listByRange.jsp?sm=3')

year = [str(year) for year in range(2000, 2019)]
value = ["26", "2", "8", "21", "28", "27", "23", "29", "30", "31", "32", "33", "S6", "S7", "S8"]

for y, v in zip(year, value):
    select_year = Select(driver.find_element_by_name('year'))
    select_coderange = Select(driver.find_element_by_name('coderange'))
    select_year.select_by_value(y)
    select_coderange.select_by_value(v)
    driver.find_element_by_xpath("/html/body/form/input[1]").click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    subject_semester = soup.select("body > table > tbody > tr > td:nth-of-type(1)")
    subject_type = soup.select("body > table > tbody > tr > td:nth-of-type(2)")
    subject_number = soup.select("body > table > tbody > tr > td:nth-of-type(3)")
    subject_name = soup.select("body > table > tbody > tr > td:nth-of-type(4) > b > a")
    subject_point = soup.select("body > table > tbody > tr > td:nth-of-type(5)")
    subject_theory = soup.select("body > table > tbody > tr > td:nth-of-type(6)")
    subject_training = soup.select("body > table > tbody > tr > td:nth-of-type(7)")
    subject_host = soup.select("body > table > tbody > tr > td:nth-of-type(8)")

    for a, b, c, d, e, f, g, h in zip(subject_semester, subject_type, subject_number, subject_name, subject_point, subject_theory, subject_training, subject_host):
        print(a.text, b.text, c.text, d.text, e.text, f.text, g.text, h.text)

driver.close()

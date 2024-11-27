'''
    코레일 접속 후 지정노선 예약가능 여부 메일 발송
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time

import gmail
import KAKAO_sendMsg.kakao_send as kakao_send

# 상수선언
DELAY = 3
REPEAT_DELAY = 60

# 노선 검색조건
ST_STATION = '수원'     # 출발역
EN_STATION = '용산'     # 도착역
YEAR = '2024'           # 예약년도
MONTH = '11'            # 예약월
DAY = '28'              # 예약일
HOUR = '0 (오전00)'     # 예약시간

driver = webdriver.Chrome()

def print_now(param):
    lt = time.localtime(time.time())
    td = time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초', lt)
    print(param % td)
    return param % td

# 로그인페이지 호출
url = "https://www.letskorail.com/korail/com/login.do"
driver.get(url)
time.sleep(DELAY)

# ID / PW 입력
xpath = '//*[@id="txtMember"]'
id = driver.find_element(By.XPATH, xpath)
id.clear()
id.send_keys('0950070766')

xpath = '//*[@id="txtPwd"]'
id = driver.find_element(By.XPATH, xpath)
id.clear()
id.send_keys('ifthen10!@')

xpath = '//*[@id="loginDisplay1"]/ul/li[3]/a/img'
id = driver.find_element(By.XPATH, xpath)
id.click()
driver.implicitly_wait(3)
print_now('로그인 : %s') 

# 승차권간편예매 검색
xpath = '//*[@id="txtGoStart"]'
id = driver.find_element(By.XPATH, xpath)
id.clear()
id.send_keys(ST_STATION)

xpath = '//*[@id="txtGoEnd"]'
id = driver.find_element(By.XPATH, xpath)
id.clear()
id.send_keys(EN_STATION)

xpath = '//*[@id="res_cont_tab01"]/form/div/fieldset/p/a/img'
id = driver.find_element(By.XPATH, xpath)
id.click()
driver.implicitly_wait(3)

# 조회조건 입력
xpath = '//*[@id="s_year"]'
selectYear = driver.find_element(By.XPATH, xpath)
select = Select(selectYear)
select.select_by_visible_text(YEAR)  # 표시된 텍스트로 선택

xpath = '//*[@id="s_month"]'
selectMonth = driver.find_element(By.XPATH, xpath)
select = Select(selectMonth)
select.select_by_visible_text(MONTH)  # 표시된 텍스트로 선택

xpath = '//*[@id="s_day"]'
selectDay = driver.find_element(By.XPATH, xpath)
select = Select(selectDay)
select.select_by_visible_text(DAY)  # 표시된 텍스트로 선택

xpath = '//*[@id="s_hour"]'
selectTime = driver.find_element(By.XPATH, xpath)
select = Select(selectTime)
select.select_by_visible_text(HOUR)  # 표시된 텍스트로 선택

# 예약조건 반복조회
while True:
    xpath = '//*[@id="center"]/div[3]/p/a/img'
    id = driver.find_element(By.XPATH, xpath)
    id.click()
    driver.implicitly_wait(3)
    
    xpath = '//*[@id="tableResult"]/tbody/tr[1]/td[6]//img'
    id = driver.find_element(By.XPATH, xpath).get_attribute('alt')
    
    xpath = '//*[@id="tableResult"]/tbody/tr[1]/td[3]'
    train_info = driver.find_element(By.XPATH, xpath).text
    
    if id == '예약하기':
        title = print_now('예약가능 : %s')
        content = '''
            출발역 : {}
            도착역 : {}
            열차정보 : {}
        '''.format(ST_STATION, EN_STATION, train_info.replace('\n', ' '))
        gmail.sendMail(title, content)
        kakao_send(content)
        break
    else:
        title = print_now('좌석매진 : %s')

    time.sleep(REPEAT_DELAY)
    
# 브라우저 종료
driver.quit()

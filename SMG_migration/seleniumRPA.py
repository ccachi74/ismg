from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert

import uiautomation as auto

import jaydebeapi
import SMG_migration.db_info as db_info
import SMG_migration.SMG_sql as SMG_sql

import time

# 상수설정
WINDOW_NAME = '열기'
COMPANY = '(주)서울문화사'
SITE_ID = db_info.SITE_ID
SITE_PW = db_info.SITE_PW

# 초기값 설정
SEQ_RANGE = (1, 10000000)
IN_PARAM = input("Upload(1) or Delete(2) : ")

# APPR_FILE 테이블 데이터 읽어오기
def get_data():
    DB_USER         = db_info.oci_info["DB_USER"]
    DB_PASSWORD     = db_info.oci_info["DB_PASSWORD"]
    DB_URL          = db_info.oci_info["DB_URL"]
    JDBC_DRIVER     = db_info.oci_info["JDBC_DRIVER"]
    JAR_FILE_PATH   = db_info.oci_info["JAR_FILE_PATH"]

    # File path to the CLOB data
    try:
        # Connect to the Oracle database using JDBC
        connection = jaydebeapi.connect(
            JDBC_DRIVER,
            DB_URL,
            [DB_USER, DB_PASSWORD],
            JAR_FILE_PATH
        )
        
        # Set autocommit to False
        connection.jconn.setAutoCommit(False)
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # 테이블 읽기
        if IN_PARAM == '1':
            cursor.execute(SMG_sql.read_data['appr_file'], SEQ_RANGE)
        else:
            cursor.execute(SMG_sql.read_data['appr_file_delete'], SEQ_RANGE)
        
        rows = cursor.fetchall()
            
    except Exception as error:
        print("Error while inserting data:", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed.")

    return rows

# APPR_FILE 테이블 업로그플래그 지우기
def update_data(docuNO):
    DB_USER         = db_info.oci_info["DB_USER"]
    DB_PASSWORD     = db_info.oci_info["DB_PASSWORD"]
    DB_URL          = db_info.oci_info["DB_URL"]
    JDBC_DRIVER     = db_info.oci_info["JDBC_DRIVER"]
    JAR_FILE_PATH   = db_info.oci_info["JAR_FILE_PATH"]

    # File path to the CLOB data
    try:
        # Connect to the Oracle database using JDBC
        connection = jaydebeapi.connect(
            JDBC_DRIVER,
            DB_URL,
            [DB_USER, DB_PASSWORD],
            JAR_FILE_PATH
        )
        
        # Set autocommit to False
        connection.jconn.setAutoCommit(False)
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # 테이블 읽기
        cursor.execute(SMG_sql.update_data['appr_file'], (docuNO,))     # 파라메터 전송 형식을 준수해야 함.
        connection.commit()
            
    except Exception as error:
        print("Error while updating data:", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed.")

def upload_file(file_name):
    """파일 업로드를 처리합니다."""
    uploader = auto.WindowControl(searchDepth=2, Name=WINDOW_NAME)

    if not uploader.Exists(3, 1):
        print('Can not find window')
        return  # 예외 처리: 윈도우를 찾지 못한 경우

    uploader.EditControl(Name="파일 이름(N):").SendKeys(file_name)
    uploader.ButtonControl(Name="열기(O)").Click()

def site_login(driver):

    # 메인페이지 호출
    url = "http://193.123.239.240:180/"
    driver.get(url)

    # 회사선택
    xpath = '//*[@id="login_intro_bg_image_container"]/div/div/form/div[1]/div/select'
    comp_field = driver.find_element(By.XPATH, xpath)
    select = Select(comp_field)
    select.select_by_visible_text(COMPANY)  # 표시된 텍스트로 선택

    # ID 입력
    id_field = driver.find_element(By.ID, "userid")
    id_field.send_keys(SITE_ID)  # 여기에 ID 입력

    # 패스워드 입력
    xpath = '//*[@id="pwd"]'
    password_field = driver.find_element(By.XPATH, xpath)
    password_field.send_keys(SITE_PW)  # 여기에 비밀번호 입력

    # 로그인 버튼 클릭
    xpath = '//*[@id="login_intro_bg_image_container"]/div/div/a'
    driver.find_element(By.XPATH, xpath).click()

    # 첨부파일 업로드 화면 호출
    url = 'http://193.123.239.240:180/gw-n/app/groupware/approval/migration/ApprovalMigAttachFileManagement.jsp'
    driver.get(url)
    driver.maximize_window()

def site_upload(driver, docuList):
    # 업로드 하기
    for docuNo in docuList:
        start_time = time.time()
        
        # 문서번호 선택 및 입력
        xpath = '/html/body/form[2]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input'
        docNo_field = driver.find_element(By.XPATH, xpath)
        docNo_field.clear()
        docNo_field.send_keys(docuNo[0])
        print(f'문서번호 : {docuNo[0]}')

        # 검색버튼 클릭
        xpath = '//*[@id="CommonBtnSearch"]'
        driver.find_element(By.XPATH, xpath).click()

        # 문서 선택 및 클릭
        xpath = '//*[@id="ifrmGridDATACell.0.0.inner"]'
        driver.find_element(By.XPATH, xpath).click()

        # iframe 내부로 진입
        xpath = '//*[@id="smodalwinContents"]'
        iframe = driver.find_element(By.XPATH, xpath)
        driver.switch_to.frame(iframe)

        # 파일업로드 버튼 클릭
        xpath = '//*[@id="filechooserContainer"]'
        driver.find_element(By.XPATH, xpath).click()

        # 업로드 파일 선택
        upload_file(docuNo[1])

        # 저장버튼 클릭
        xpath = '//*[@id="CommonBtnSave"]'
        driver.find_element(By.XPATH, xpath).click()

        # iframe 밖으로 다시 나오기
        driver.switch_to.default_content()
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"수행 시간: {execution_time:.6f}초")

# 업로드 파일 삭제
def site_delete(driver, docuList):
    for docuNo in docuList:
        start_time = time.time()
        
        # 문서번호 선택 및 입력
        xpath = '/html/body/form[2]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input'
        docNo_field = driver.find_element(By.XPATH, xpath)
        docNo_field.clear()
        docNo_field.send_keys(docuNo[0])
        print(f'문서번호 : {docuNo[0]}')

        # 검색버튼 클릭
        xpath = '//*[@id="CommonBtnSearch"]'
        driver.find_element(By.XPATH, xpath).click()

        # 문서 선택 및 클릭
        xpath = '//*[@id="ifrmGridDATACell.0.0.inner"]'
        driver.find_element(By.XPATH, xpath).click()

        # iframe 내부로 진입
        xpath = '//*[@id="smodalwinContents"]'
        iframe = driver.find_element(By.XPATH, xpath)
        driver.switch_to.frame(iframe)

        # 파일삭제 버튼 클릭
        xpath = '//*[@id="file-upload-list-data"]/tr/td[1]/img'
        driver.find_element(By.XPATH, xpath).click()

        # 메세지박스 확인버튼 클릭
        Alert(driver).accept()
        
        # 플래그 업데이트
        update_data(docuNo[0])
        
        # 저장버튼 클릭
        xpath = '//*[@id="CommonBtnSave"]'
        driver.find_element(By.XPATH, xpath).click()

        # iframe 밖으로 다시 나오기
        driver.switch_to.default_content()
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"수행 시간: {execution_time:.6f}초")
    
def main():
    driver = webdriver.Chrome()
    driver.implicitly_wait(60)

    site_login(driver)              # 사이트접속
    docuList = get_data()           # 첨부파일 목록 읽어오기

    if IN_PARAM == '1':
        site_upload(driver, docuList)               # 첨부파일 저장
    else:
        site_delete(driver, docuList)               # 첨부파일 삭제
    
    # 브라우저 종료
    driver.quit()
    
if __name__ == "__main__":
    main()
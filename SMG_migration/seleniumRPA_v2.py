import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import uiautomation as auto
import jaydebeapi
import db_info as db_info
import SMG_sql as SMG_sql
import time

# 상수설정
WINDOW_NAME = '열기'
DELAY_TIME = 3
COMPANY = '(주)서울문화사'
SITE_ID = db_info.SITE_ID
SITE_PW = db_info.SITE_PW

# 초기값 설정
SEQ_RANGE = (1, 10000000)

IN_PARAM = None  # 초기화

# Tkinter GUI 설정
class MigrationBot:
    def __init__(self, master):
        self.master = master
        master.title("SMG Migration Bot")
        master.geometry("400x650+1400+5")
        
        icon32 = tk.PhotoImage(file='logo14.png')
        master.iconphoto(False, icon32)

        self.label1 = tk.Label(master, text="Input SEQ_RANGE (Start, End):")
        self.label1.pack()

        self.seq_range_entry = tk.Entry(master)
        self.seq_range_entry.pack()

        # 라디오 버튼 추가
        self.in_param_entry = tk.StringVar(value="1")  # 기본값 설정
        self.upload_radio = tk.Radiobutton(master, text="Upload", variable=self.in_param_entry, value="1")
        self.upload_radio.pack()
        
        self.delete_radio = tk.Radiobutton(master, text="Delete", variable=self.in_param_entry, value="2")
        self.delete_radio.pack()
        
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

        # 텍스트 위젯 추가
        self.text_widget = tk.Text(master, state="disabled", bg="black", fg="white", font=("맑은 고딕", 10))
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # 종료 버튼 추가
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack(pady=10)
    
    def submit(self):
        global SEQ_RANGE, IN_PARAM
        try:
            # SEQ_RANGE 입력 처리
            SEQ_RANGE = tuple(map(int, self.seq_range_entry.get().split(',')))
            # IN_PARAM 입력 처리
            IN_PARAM = self.in_param_entry.get()
            
            self.start_selenium_process()  # Selenium 작업 시작
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_selenium_process(self):
        self.log("Starting Selenium...")

        """Selenium 작업을 시작하는 메서드"""
        driver = webdriver.Chrome()
        driver.implicitly_wait(60)
        
        site_login(driver, self)                # 사이트접속
        docuList = get_data(self)               # 첨부파일 목록 읽어오기

        if IN_PARAM == '1':
            site_upload(driver, docuList, self)               # 첨부파일 저장
        else:
            site_delete(driver, docuList, self)               # 첨부파일 삭제
        
        # 브라우저 종료
        driver.quit()
        
    def exit_application(self):
        """종료 버튼 클릭 시 실행"""
        self.master.quit()  # GUI 종료
        
    def log(self, message):
        """텍스트 위젯에 로그 메시지 출력"""
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", message + "\n")
        self.text_widget.config(state="disabled")
        self.text_widget.see("end")
        self.master.update_idletasks()  # GUI 업데이트
                    
# APPR_FILE 테이블 데이터 읽어오기
def get_data(app):
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
        app.log("Error while inserting data:", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            app.log("DB connection closed.")

    return rows

# APPR_FILE 테이블 업로드 플래그 지우기
def update_data(docuNO, app):
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
        app.log("Error while updating data:", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            app.log("DB Update complete.")

def upload_file(file_name, app):
    """파일 업로드를 처리합니다."""
    uploader = auto.WindowControl(searchDepth=2, Name=WINDOW_NAME)

    if not uploader.Exists(3, 1):
        app.log('Can not find window')
        return  # 예외 처리: 윈도우를 찾지 못한 경우

    uploader.EditControl(Name="파일 이름(N):").SendKeys(file_name)
    uploader.ButtonControl(Name="열기(O)").Click()

def site_login(driver, app):

    # 메인페이지 호출
    # url = "http://193.123.239.240:180/"
    url = "https://gw.mlounge.co.kr/"
    driver.get(url)

    time.sleep(DELAY_TIME)

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
    xpath = '//*[@id="login_intro_bg_image_container"]/div/div/form/a'
    driver.find_element(By.XPATH, xpath).click()
    time.sleep(DELAY_TIME)

    # 첨부파일 업로드 화면 호출
    # url = 'http://193.123.239.240:180/gw-n/app/groupware/approval/migration/ApprovalMigAttachFileManagement.jsp'
    url = 'https://gw.mlounge.co.kr/gw-n/app/groupware/approval/migration/ApprovalMigAttachFileManagement.jsp'
    driver.get(url)
    # driver.maximize_window()
    time.sleep(DELAY_TIME)
    
    app.log("Login Complete.")

def site_upload(driver, docuList, app):
    # 업로드 하기
    for counter, docuNo in enumerate(docuList):
        tm = time.localtime()
        app.log(f'현재시간 : {tm.tm_year}.{tm.tm_mon}.{tm.tm_mday} {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}')
        
        start_time = time.time()
        
        # 문서번호 선택 및 입력
        xpath = '/html/body/form[2]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input'
        docNo_field = driver.find_element(By.XPATH, xpath)
        docNo_field.clear()
        docNo_field.send_keys(docuNo[0])
        app.log(f'문서번호 : {docuNo[0]}')

        # 검색버튼 클릭
        xpath = '//*[@id="CommonBtnSearch"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(DELAY_TIME)

        # 문서 선택 및 클릭
        xpath = '//*[@id="ifrmGridDATACell.0.0.inner"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(DELAY_TIME)

        # iframe 내부로 진입
        xpath = '//*[@id="smodalwinContents"]'
        iframe = driver.find_element(By.XPATH, xpath)
        driver.switch_to.frame(iframe)

        # 파일업로드 버튼 클릭
        xpath = '//*[@id="filechooserContainer"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(DELAY_TIME)

        # 업로드 파일 선택
        upload_file(docuNo[1], app)

        # 저장버튼 클릭
        xpath = '//*[@id="CommonBtnSave"]'
        driver.find_element(By.XPATH, xpath).click()
        
        # 첨부파일 용량에 따라 대기시간 조정
        if docuNo[4] < 15000000:
            time.sleep(DELAY_TIME*2)
        else:
            tm = int((docuNo[4] + 15000000) / 15000000)
            time.sleep(DELAY_TIME*2+tm)
            
        app.log(f"파일용량 : {docuNo[4]} Byte")
        app.log(f"처리현황 : {counter+1} / {len(docuList)}")

        # iframe 밖으로 다시 나오기
        driver.switch_to.default_content()
                
        end_time = time.time()
        execution_time = end_time - start_time
        app.log(f"수행시간 : {execution_time:.6f}초")

    time.sleep(DELAY_TIME)

# 업로드 파일 삭제
def site_delete(driver, docuList, app):
    for docuNo in docuList:
        start_time = time.time()
        
        # 문서번호 선택 및 입력
        xpath = '/html/body/form[2]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input'
        docNo_field = driver.find_element(By.XPATH, xpath)
        docNo_field.clear()
        docNo_field.send_keys(docuNo[0])
        app.log(f'문서번호 : {docuNo[0]}')

        # 검색버튼 클릭
        xpath = '//*[@id="CommonBtnSearch"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(DELAY_TIME)

        # 문서 선택 및 클릭
        xpath = '//*[@id="ifrmGridDATACell.0.0.inner"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(DELAY_TIME)

        # iframe 내부로 진입
        xpath = '//*[@id="smodalwinContents"]'
        iframe = driver.find_element(By.XPATH, xpath)
        driver.switch_to.frame(iframe)

        # 파일삭제 버튼 클릭
        xpath = '//*[@id="file-upload-list-data"]/tr/td[1]/img'
        driver.find_element(By.XPATH, xpath).click()

        # 메세지박스 확인버튼 클릭
        Alert(driver).accept()
        time.sleep(DELAY_TIME)
        
        # 플래그 업데이트
        update_data(docuNo[0], app)
        
        # 저장버튼 클릭
        xpath = '//*[@id="CommonBtnSave"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(DELAY_TIME)

        # iframe 밖으로 다시 나오기
        driver.switch_to.default_content()
        
        end_time = time.time()
        execution_time = end_time - start_time
        app.log(f"수행시간 : {execution_time:.6f}초")

    time.sleep(DELAY_TIME)
    
def main():
    # Tkinter GUI 실행
    root = tk.Tk()
    app = MigrationBot(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
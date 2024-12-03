import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import gmail
import setInfo
import threading

# Tkinter GUI 앱 클래스
class KorailApp:
    def __init__(self, root, REPEAT_DELAY=60):
        self.root = root
        self.REPEAT_DELAY = REPEAT_DELAY
        
        self.root.title("Korail Reservation Checker")
        
        icon32 = tk.PhotoImage(file='logo14.png')
        self.root.iconphoto(False, icon32)
        
        self.root.geometry("800x650+1000+5")
        self.driver = None  # Selenium 드라이버 초기화

        # 입력 영역
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # 오늘 날짜 가져오기
        today = datetime.today()
        self.YEAR = today.year
        self.MONTH = today.month
        self.DAY = today.day

        # Label과 Entry 위젯
        tk.Label(input_frame, text="Year:").grid(row=0, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=10)
        self.year_entry.grid(row=0, column=1, padx=5, pady=5)
        self.year_entry.insert(0, str(self.YEAR))  # 오늘 날짜의 년도 입력

        tk.Label(input_frame, text="Month:").grid(row=0, column=2, padx=5, pady=5)
        self.month_entry = tk.Entry(input_frame, width=10)
        self.month_entry.grid(row=0, column=3, padx=5, pady=5)
        self.month_entry.insert(0, str(self.MONTH))  # 오늘 날짜의 월 입력

        tk.Label(input_frame, text="Day:").grid(row=0, column=4, padx=5, pady=5)
        self.day_entry = tk.Entry(input_frame, width=10)
        self.day_entry.grid(row=0, column=5, padx=5, pady=5)
        self.day_entry.insert(0, str(self.DAY))  # 오늘 날짜의 일 입력

        # 출근/퇴근 라디오 버튼
        self.attendance_status = tk.StringVar(value="출근")  # 기본값은 "출근"
        tk.Radiobutton(input_frame, text="출근", variable=self.attendance_status, value="출근").grid(row=1, column=0, columnspan=2, pady=5)
        tk.Radiobutton(input_frame, text="퇴근", variable=self.attendance_status, value="퇴근").grid(row=1, column=2, columnspan=2, pady=5)

        # 확인 버튼
        submit_button = tk.Button(input_frame, text="Submit", command=self.submit_date)
        submit_button.grid(row=1, column=4, columnspan=2, padx=10, pady=5)

        # 텍스트 출력 위젯
        self.text_widget = tk.Text(self.root, state="disabled", bg="black", fg="white", font=("맑은 고딕", 10))
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # 스크롤바 추가
        self.scrollbar = tk.Scrollbar(self.text_widget, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        
        # 종료 버튼
        self.exit_button = tk.Button(self.root, text="종료", command=self.exit_application, font=("맑은 고딕", 10))
        self.exit_button.pack(pady=10)
        
    def submit_date(self):
        """입력된 날짜와 출근/퇴근 상태를 처리"""
        self.YEAR = self.year_entry.get().strip()
        self.MONTH = self.month_entry.get().strip()
        self.DAY = self.day_entry.get().strip()
        self.STATUS = self.attendance_status.get()  # 출근/퇴근 상태

        if self.STATUS == '출근':
            self.ST_STATION = '수원'
            self.EN_STATION = '용산'
            self.HOUR = '0 (오전00)'
            self.TR_LINE = 1
        elif self.STATUS == '퇴근':
            self.ST_STATION = '용산'
            self.EN_STATION = '수원'
            self.HOUR = '18 (오후06)'
            self.TR_LINE = 2
        else:
            messagebox.showerror("Input Error", "올바른 값을 입력하세요. (1 또는 2)")
            self.root.destroy()
            return

        # 유효성 검사
        if not (self.YEAR.isdigit() and self.MONTH.isdigit() and self.DAY.isdigit()):
            messagebox.showerror("Input Error", "Please enter valid numeric values for Year, Month, and Day.")
            return

        # Text 위젯에 출력
        self.log(f"Date: {self.YEAR}-{self.MONTH.zfill(2)}-{self.DAY.zfill(2)} - Status: {self.STATUS}")
        
        self.start_thread()
        
    def log(self, message):
        """텍스트 위젯에 로그 메시지 출력"""
        self.text_widget.config(state="normal")
        
        if '예약가능' in message:
            self.text_widget.insert("end", message + "\n", "green")
        else:
            self.text_widget.insert("end", message + "\n", "white")
            
        self.text_widget.config(state="disabled")
        self.text_widget.see("end")
        self.text_widget.tag_configure("green", foreground="green")  # 녹색 태그 설정
        self.text_widget.tag_configure("white", foreground="white")  # 흰색 태그 설정
        self.root.update_idletasks()  # 화면 강제 갱신

    def start_thread(self):
        """Selenium 작업을 별도의 스레드에서 실행"""
        thread = threading.Thread(target=self.start_process)
        thread.daemon = True  # 메인 프로세스 종료 시 강제 종료
        thread.start()
        
    def start_process(self):
        """예약 확인 프로세스 시작"""
        try:
            # Selenium 드라이버 설정
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)

            self.log("크롬 드라이버 시작...")
            
            # 로그인 페이지 호출
            url = "https://www.letskorail.com/korail/com/login.do"
            self.driver.get(url)

            # 로그인 정보 입력
            self.log(f"로그인 : {datetime.today()}")
            self.driver.find_element(By.XPATH, '//*[@id="txtMember"]').send_keys(setInfo.ID)
            self.driver.find_element(By.XPATH, '//*[@id="txtPwd"]').send_keys(setInfo.PW)
            self.driver.find_element(By.XPATH, '//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()

            # 검색 조건 입력
            self.driver.find_element(By.XPATH, '//*[@id="txtGoStart"]').clear()
            self.driver.find_element(By.XPATH, '//*[@id="txtGoStart"]').send_keys(self.ST_STATION)
            self.driver.find_element(By.XPATH, '//*[@id="txtGoEnd"]').clear()
            self.driver.find_element(By.XPATH, '//*[@id="txtGoEnd"]').send_keys(self.EN_STATION)
            self.driver.find_element(By.XPATH, '//*[@id="res_cont_tab01"]/form/div/fieldset/p/a/img').click()

            # 예약 날짜와 시간 설정
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="s_year"]')))
            Select(element).select_by_visible_text(self.YEAR)
            # Select(self.driver.find_element(By.XPATH, '//*[@id="s_year"]')).select_by_visible_text(self.YEAR)
            Select(self.driver.find_element(By.XPATH, '//*[@id="s_month"]')).select_by_visible_text(self.MONTH)
            Select(self.driver.find_element(By.XPATH, '//*[@id="s_day"]')).select_by_visible_text(self.DAY)
            Select(self.driver.find_element(By.XPATH, '//*[@id="s_hour"]')).select_by_visible_text(self.HOUR)

            # 반복 조회
            while True:
                if not self.driver:
                    break
                self.driver.find_element(By.XPATH, '//*[@id="center"]/div[3]/p/a/img').click()

                # 예약 상태 확인
                status = self.driver.find_element(By.XPATH, f'//*[@id="tableResult"]/tbody/tr[{self.TR_LINE}]/td[6]//img').get_attribute('alt')
                train_info = self.driver.find_element(By.XPATH, f'//*[@id="tableResult"]/tbody/tr[{self.TR_LINE}]/td[3]').text.replace('\n', ' ')

                content = f'''
                출발역 : {self.ST_STATION}
                도착역 : {self.EN_STATION}
                예약일 : {self.YEAR}년 {self.MONTH}월 {self.DAY}일
                열차정보 : {train_info}
                '''

                if status == '예약하기':
                    title = f"예약가능 : {datetime.today()}"
                    self.log(title)
                    self.log(content)
                    gmail.sendMail(title, content)
                    break
                else:
                    title = f"좌석매진 : {datetime.today()}"
                    self.log(title)
                    self.log(content)

                time.sleep(self.REPEAT_DELAY)

        except Exception as e:
            self.log(f"오류 발생: {e}")
        finally:
            self.log("프로세스 종료")
            self.driver.quit()
            self.driver = None

    def exit_application(self):
        """종료 버튼 클릭 시 실행"""
        if self.driver:
            self.driver.quit()  # Selenium 드라이버 종료
            self.driver = None
        self.log("애플리케이션 종료.")
        self.root.destroy()  # GUI 종료
        
# GUI 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = KorailApp(root)
    root.mainloop()

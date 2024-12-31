import os
import jaydebeapi
import json
import tkinter as tk
from tkinter import filedialog
import datetime

import db_info as db_info
import SMG_sql as SMG_sql

def unix2date(unix_time):
    if unix_time == '0':
        date_time = "영구"
    elif unix_time:
        date_time = datetime.datetime.fromtimestamp(int(unix_time))
    else:
        date_time = ''
    
    return date_time

def select_folder():
    # Tkinter 창을 숨기기 위한 코드
    root = tk.Tk()
    root.withdraw()  # 기본 Tkinter 창 숨기기

    # 폴더 선택 대화 상자 열기
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        print("선택한 폴더 경로:", folder_path)
    else:
        print("폴더가 선택되지 않았습니다.")
    return folder_path

def find_files(directory, extention1, extention2):
    result_files_1 = []
    result_files_2 = []
    
    # 디렉토리와 하위 디렉토리 모두 검색
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extention1):
                # 파일의 전체 경로를 저장
                result_files_1.append(os.path.join(root, file))
            if file.lower().endswith(extention2):
                # 파일의 전체 경로를 저장
                result_files_2.append(os.path.join(root, file))
    
    print(f"{extention1} : {len(result_files_1)}")
    print(f"{extention2} : {len(result_files_2)}")
    
    return result_files_1, result_files_2

def extract_filename_from_path(file_path):
    # os.path.basename() 함수를 사용하여 파일명만 추출
    return os.path.basename(file_path)

def check_file_exists(file_path):
    """주어진 파일 경로가 존재하는지 확인하는 함수"""
    if not os.path.isfile(file_path):
        print(f"파일이 존재하지 않습니다: {file_path}")
        return "N"
    return "Y"

def get_file_size(file_path):
    if not os.path.isfile(file_path):
        return 0
    return os.path.getsize(file_path)
    
# Main Process
def main():
    directory = select_folder()                                 # 작업대상폴더 선택
    sel_db = input("Select DBMS(1: OCI, 2: postgres) : ")       # Database 선택
    
    mht_file_list, json_file_list = find_files(directory, '.mht', '.json')

    counter = 0
    total_cnt = len(json_file_list)
    
    # Database connection details
    if  sel_db == "1":
        DB_USER         = db_info.oci_info["DB_USER"]
        DB_PASSWORD     = db_info.oci_info["DB_PASSWORD"]
        DB_URL          = db_info.oci_info["DB_URL"]
        JDBC_DRIVER     = db_info.oci_info["JDBC_DRIVER"]
        JAR_FILE_PATH   = db_info.oci_info["JAR_FILE_PATH"]
    elif sel_db == "2":
        DB_USER         = db_info.postgres_jdbc_info["DB_USER"]
        DB_PASSWORD     = db_info.postgres_jdbc_info["DB_PASSWORD"]
        DB_URL          = db_info.postgres_jdbc_info["DB_URL"]
        JDBC_DRIVER     = db_info.postgres_jdbc_info["JDBC_DRIVER"]
        JAR_FILE_PATH   = db_info.postgres_jdbc_info["JAR_FILE_PATH"]
    else:
        return
    
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
                
        # Read CLOB data from the file
        for file_path, json_file_path in zip(mht_file_list, json_file_list):

            # json_file_name = extract_filename_from_path(json_file_path)
            with open(json_file_path, 'r', encoding='utf-8') as file_json:
                json_data = json.load(file_json)

            # Insert data into table (첨부파일정보)
            for file in json_data.get('files'):
                insert_query = SMG_sql.update_data['appr_file_size']
                path = str(os.path.join(os.path.dirname(file_path), file)).replace('/', '\\')
                
                # if check_file_exists(path):
                cursor.execute(insert_query, (
                    get_file_size(path),
                    path
                    ))
                
                connection.commit()
                
            counter += 1
            print(f"Data inserted successfully. ({counter} / {total_cnt})")

    except Exception as error:
        print("Error while inserting data:", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            if sel_db == '1':
                print("OCI connection closed.")
            else:
                print("postgres connection closed.")
            
if __name__ == "__main__":
    main()
    input('아무 키나 누르세요...')
    
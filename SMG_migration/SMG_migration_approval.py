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

def find_files(directory, extention):
    result_files = []
    
    # 디렉토리와 하위 디렉토리 모두 검색
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extention):
                # 파일의 전체 경로를 저장
                result_files.append(os.path.join(root, file))
    
    print(f"{extention} : {len(result_files)}")
    
    return result_files

def extract_filename_from_path(file_path):
    # os.path.basename() 함수를 사용하여 파일명만 추출
    return os.path.basename(file_path)

# Main Process
def main():
    seq = 0
    
    directory = select_folder()                                 # 작업대상폴더 선택
    sel_db = input("Select DBMS(1: OCI, 2: postgres) : ")       # Database 선택
    truncate_flag = input("Truncate Table (y or n) ? ")         # DB Truncate 설정    
    seq = int(input("Start with File Seq No. : "))              # 일련번호 초기값 설정
    
    mht_file_list = find_files(directory, '.mht')
    json_file_list = find_files(directory, '.json')

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
        
        # 테이블 초기화
        if truncate_flag == "y":
            for trunc_query in SMG_sql.migration_truncate.values():
                cursor.execute(trunc_query)
            
            connection.commit()
        
        # Read CLOB data from the file
        for file_path, json_file_path in zip(mht_file_list, json_file_list):
            file_name = extract_filename_from_path(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                large_text_data = file.read()

            # json_file_name = extract_filename_from_path(json_file_path)
            with open(json_file_path, 'r', encoding='utf-8') as file_json:
                json_data = json.load(file_json)

            # Insert data into table (결재기본정보)
            insert_query = SMG_sql.migration_insert['appr_header']
            
            # print(json_data.get('title'))
            print(file_path)

            cursor.execute(insert_query, (
                file_name, 
                large_text_data, 
                json_data.get('title'),
                json_data.get('type'),
                json_data.get('formCode'),
                json_data.get('formName'),
                json_data.get('docuNo') + '/' + str(unix2date(json_data.get('draftDay'))),
                json_data.get('drafterNo'),
                json_data.get('drafter'),
                json_data.get('drafterGroupNo'),
                json_data.get('draftGroupName'),
                str(unix2date(json_data.get('draftDay'))),
                str(unix2date(json_data.get('aprvDay'))),
                str(unix2date(json_data.get('expireDay'))),
                json_data.get('public'),
                json_data.get('step'),
                json_data.get('extraData')
                ))

            connection.commit()

            # Insert data into table (결재선정보)
            for line in json_data.get('lines'):
                insert_query = SMG_sql.migration_insert['appr_line']
                
                cursor.execute(insert_query, (
                json_data.get('docuNo') + '/' + str(unix2date(json_data.get('draftDay'))),
                    line.get('userNo'),
                    line.get('userName'),
                    line.get('groupNo'),
                    line.get('groupName'),
                    line.get('position'),
                    line.get('duty'),
                    line.get('order'),
                    line.get('seq'),
                    line.get('method'),
                    str(unix2date(line.get('date'))),
                    line.get('result')
                    ))
                            
                connection.commit()
                
            # Insert data into table (결재참조자정보)
            for refer in json_data.get('refers'):
                insert_query = SMG_sql.migration_insert['appr_refer']

                cursor.execute(insert_query, (
                json_data.get('docuNo') + '/' + str(unix2date(json_data.get('draftDay'))),
                    refer.get('userNo'),
                    refer.get('userName'),
                    refer.get('groupNo'),
                    refer.get('groupName')
                    ))
                
                connection.commit()

            # Insert data into table (결재열람자정보)
            for view in json_data.get('views'):
                insert_query = SMG_sql.migration_insert['appr_view']

                cursor.execute(insert_query, (
                json_data.get('docuNo') + '/' + str(unix2date(json_data.get('draftDay'))),
                    view.get('userNo'),
                    view.get('userName'),
                    view.get('groupNo'),
                    view.get('groupName')
                    ))
                
                connection.commit()

            # Insert data into table (첨부파일정보)
            for file in json_data.get('files'):
                seq = seq + 1
                insert_query = SMG_sql.migration_insert['appr_file']
                
                cursor.execute(insert_query, (
                json_data.get('docuNo') + '/' + str(unix2date(json_data.get('draftDay'))),
                    file,
                    str(os.path.join(os.path.dirname(file_path), file)).replace('/', '\\'),
                    seq
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
    
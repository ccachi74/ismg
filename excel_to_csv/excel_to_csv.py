import os
import pandas as pd

# 변환할 Excel 파일이 있는 폴더 경로
input_folder = r'C:\ismg\작가정산_AS-IS Table 백업'  # 여기에 Excel 파일이 있는 폴더 경로를 입력하세요
output_folder = r'C:\ismg\작가정산_AS-IS Table 백업\csv'    # 여기에 변환된 CSV 파일을 저장할 폴더 경로를 입력하세요

# 출력 폴더가 존재하지 않으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 폴더 내의 모든 파일을 확인
for filename in os.listdir(input_folder):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):  # Excel 파일 확장자 확인
        excel_file_path = os.path.join(input_folder, filename)
        
        # Excel 파일 읽기
        df = pd.read_excel(excel_file_path)
        
        # CSV 파일로 저장
        csv_file_name = os.path.splitext(filename)[0] + '.csv'  # 파일 이름 변경
        csv_file_path = os.path.join(output_folder, csv_file_name)
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')  # index=False로 인덱스 열을 저장하지 않음
        
        print(f'Converted {filename} to {csv_file_name}')
# 20260820 12:00
# ==========================================================
# [scripts/excel_to_mysql.py]
# 엑셀 데이터 -> MySQL flood_shelter (표준 컬럼) 일괄 적재
# ==========================================================

import os
# 표 형태의 데이터를 다루는 pandas 라이브러리 로드
import pandas as pd
# MySQL DB 연결 도구 로드
from sqlalchemy import create_engine

# 1. 엑셀 파일 폴더 경로
FOLDER_PATH = "scripts"

# 2. MySQL 접속 URL (본인의 실제 root 비밀번호를 입력해주세요)
DB_URL = "mysql+pymysql://root:root@localhost:3306/shelter_project"

def run_etl():
    print("=" * 60)
    print("🚀 [Step 1] 엑셀 데이터 파일 로드 시작")
    print("=" * 60)

    # scripts 폴더에서 flood_shelter 엑셀 파일 찾기
    target_file = None
    for f in os.listdir(FOLDER_PATH):
        if f.startswith("flood_shelter") and (f.endswith(".xlsx") or f.endswith(".xls")):
            target_file = os.path.join(FOLDER_PATH, f)
            break

    if not target_file:
        print("❌ flood_shelter 엑셀 파일을 찾을 수 없습니다.")
        return

    # 엑셀 파일 읽기
    raw_df = pd.read_excel(target_file, engine='openpyxl')
    print(f"📄 원본 엑셀 데이터 {len(raw_df):,}건 로드 완료")

    print("\n🧹 [Step 2] MySQL 컬럼 규격에 맞춰 데이터 정제 중...")
    clean_df = pd.DataFrame()

    # 우리가 만든 MySQL 테이블 컬럼과 1:1로 정확하게 매핑
    clean_df['ctpv_nm'] = raw_df['ctpv_nm'].astype(str)
    clean_df['sgg_nm'] = raw_df['sgg_nm'].astype(str)
    clean_df['fclt_nm'] = raw_df['fclt_nm'].astype(str)
    clean_df['daddr'] = raw_df['daddr'].astype(str)
    
    # 위도(lat)와 경도(lot)는 소수점 숫자형(Float)으로 변환
    clean_df['lot'] = pd.to_numeric(raw_df['lot'], errors='coerce')
    clean_df['lat'] = pd.to_numeric(raw_df['lat'], errors='coerce')
    clean_df['mng_dept_nm'] = raw_df['mng_dept_nm'].fillna('미지정')

    # 위도, 경도, 시설명이 없는 불량 데이터(결측치) 행 제거
    clean_df = clean_df.dropna(subset=['lat', 'lot', 'fclt_nm'])

    print(f"✨ 정제 완료: 유효 데이터 {len(clean_df):,}건 준비됨")

    print("\n💾 [Step 3] MySQL flood_shelter 테이블에 데이터 밀어 넣기...")
    engine = create_engine(DB_URL)

    # if_exists='append': 우리가 Workbench에서 만든 테이블 구조를 유지하면서 데이터만 쏙 채워 넣음
    # index=False: 파이썬 행 번호는 제외 (shlt_id는 DB가 1, 2, 3... 자동 증가로 채움)
    clean_df.to_sql(name='flood_shelter', con=engine, if_exists='append', index=False)

    print("=" * 60)
    print(f"🎉 대성공! 총 {len(clean_df):,}건이 'flood_shelter' 테이블에 완벽하게 저장되었습니다!")
    print("=" * 60)

if __name__ == "__main__":
    run_etl()
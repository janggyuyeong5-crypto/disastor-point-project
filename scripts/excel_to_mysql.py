# ==========================================================
# [scripts/excel_to_mysql.py]
# 엑셀 데이터 -> MySQL flood_shelter (se 컬럼 포함) 일괄 적재
# ==========================================================

import os
import urllib.parse
# 1. 표 형태의 엑셀 데이터를 가공하기 위한 pandas 라이브러리 로드[cite: 6]
import pandas as pd
# 2. 파이썬과 MySQL을 연결해주는 SQLAlchemy 엔진 로드[cite: 6]
from sqlalchemy import create_engine

# --- [DB 접속 정보 설정] ---
DB_USER = "root"
DB_PASSWORD = "root"  # 본인의 MySQL root 비밀번호[cite: 6]
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "shelter_project"

# 비밀번호 특수문자 안전 인코딩
encoded_pw = urllib.parse.quote_plus(DB_PASSWORD)
DB_URL = f"mysql+pymysql://{DB_USER}:{encoded_pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

FOLDER_PATH = "scripts"

def run_etl():
    print("=" * 65)
    print("🚀 [Step 1] 엑셀 데이터 파일 탐색 및 로드 시작")
    print("=" * 65)

    # scripts 폴더에서 flood_shelter 엑셀 파일 찾기[cite: 6]
    target_file = None
    for f in os.listdir(FOLDER_PATH):
        if f.startswith("flood_shelter") and (f.endswith(".xlsx") or f.endswith(".xls")):
            target_file = os.path.join(FOLDER_PATH, f)
            break

    if not target_file:
        print("❌ flood_shelter 엑셀 파일을 찾을 수 없습니다.")
        return

    # 엑셀 파일 읽기[cite: 6]
    raw_df = pd.read_excel(target_file, engine='openpyxl')
    print(f"📄 원본 엑셀 데이터 {len(raw_df):,}건 로드 완료")

    print("\n🧹 [Step 2] MySQL 규격에 맞춰 데이터 정제 및 se 컬럼 추가 중...")
    clean_df = pd.DataFrame()

    # 1) 기본 문자열 컬럼 정제[cite: 6]
    clean_df['ctpv_nm'] = raw_df['ctpv_nm'].astype(str)
    clean_df['sgg_nm'] = raw_df['sgg_nm'].astype(str)
    clean_df['fclt_nm'] = raw_df['fclt_nm'].astype(str)
    clean_df['daddr'] = raw_df['daddr'].astype(str)
    
    # 2) 위도(lat)와 경도(lot) 숫자형(Float) 변환[cite: 6]
    clean_df['lot'] = pd.to_numeric(raw_df['lot'], errors='coerce')
    clean_df['lat'] = pd.to_numeric(raw_df['lat'], errors='coerce')
    
    # 3) 관리부서명 결측치(NaN) 처리[cite: 6]
    clean_df['mng_dept_nm'] = raw_df['mng_dept_nm'].fillna('미지정')

    # 4) 🌟 [신규 추가] 대피소 구분 코드(se) 정제 (결측 시 3으로 채우고 정수형 변환)
    if 'se' in raw_df.columns:
        clean_df['se'] = pd.to_numeric(raw_df['se'], errors='coerce').fillna(3).astype(int)
    else:
        clean_df['se'] = 3

    # 5) 필수 결측치(위도, 경도, 시설명) 행 제거[cite: 6]
    clean_df = clean_df.dropna(subset=['lat', 'lot', 'fclt_nm'])

    print(f"✨ 정제 완료: 유효 데이터 {len(clean_df):,}건 준비됨 (se 컬럼 포함)")

    print("\n💾 [Step 3] MySQL flood_shelter 테이블에 데이터 적재 중...")
    try:
        engine = create_engine(DB_URL)

        # if_exists='append': 테이블의 shlt_id 자동증가(AUTO_INCREMENT)를 유지하며 데이터 삽입[cite: 6]
        # index=False: 파이썬 내부 인덱스는 제외[cite: 6]
        clean_df.to_sql(name='flood_shelter', con=engine, if_exists='append', index=False)

        print("=" * 65)
        print(f"🎉 [성공!] 총 {len(clean_df):,}건이 'flood_shelter' 테이블에 완벽하게 저장되었습니다!")
        print("=" * 65)

    except Exception as e:
        print(f"❌ DB 저장 에러: {e}")

if __name__ == "__main__":
    run_etl()
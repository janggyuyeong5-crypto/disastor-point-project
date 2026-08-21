import os
import urllib.parse
import pandas as pd
from sqlalchemy import create_engine

# --- [DB 접속 정보 설정] ---
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "shelter_db"

encoded_pw = urllib.parse.quote_plus(DB_PASSWORD)
DB_URL = f"mysql+pymysql://{DB_USER}:{encoded_pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

FOLDER_PATH = "scripts"

def run_etl():
    print("=" * 65)
    print("🚀 [Step 1] 홍수 엑셀 데이터 파일 탐색 및 로드 시작")
    print("=" * 65)

    target_file = None
    for f in os.listdir(FOLDER_PATH):
        if f.startswith("flood_shelter") and (f.endswith(".xlsx") or f.endswith(".xls")):
            target_file = os.path.join(FOLDER_PATH, f)
            break

    if not target_file:
        print("❌ flood_shelter 엑셀 파일을 찾을 수 없습니다.")
        return

    raw_df = pd.read_excel(target_file, engine='openpyxl')
    print(f"📄 원본 엑셀 데이터 {len(raw_df):,}건 로드 완료")

    print("\n🧹 [Step 2] MySQL 규격에 맞춰 데이터 정제 중...")
    clean_df = pd.DataFrame()

    clean_df['ctpv_nm'] = raw_df['ctpv_nm'].astype(str)
    clean_df['sgg_nm'] = raw_df['sgg_nm'].astype(str)
    clean_df['fclt_nm'] = raw_df['fclt_nm'].astype(str)
    clean_df['daddr'] = raw_df['daddr'].astype(str)
    clean_df['lot'] = pd.to_numeric(raw_df['lot'], errors='coerce')
    clean_df['lat'] = pd.to_numeric(raw_df['lat'], errors='coerce')
    
    # [요청사항 반영] 관리부서 '-', 구분코드 3
    clean_df['mng_dept_nm'] = '-'
    clean_df['se'] = 3

    clean_df = clean_df.dropna(subset=['lat', 'lot', 'fclt_nm'])

    print(f"✨ 정제 완료: 유효 데이터 {len(clean_df):,}건")

    print("\n💾 [Step 3] MySQL flood 테이블에 데이터 적재 중...")
    try:
        engine = create_engine(DB_URL)
        
        # 컬럼 순서 정렬
        column_order = ['ctpv_nm', 'sgg_nm', 'fclt_nm', 'daddr', 'lot', 'lat', 'mng_dept_nm', 'se']
        clean_df = clean_df[column_order]

        clean_df.to_sql(name='flood', con=engine, if_exists='append', index=False)
        print("🎉 [성공!] 'flood' 테이블에 저장되었습니다!")
    except Exception as e:
        print(f"❌ DB 저장 에러: {e}")

if __name__ == "__main__":
    run_etl()
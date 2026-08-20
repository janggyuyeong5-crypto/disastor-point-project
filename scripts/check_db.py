# ==========================================================
# [scripts/check_db.py] MySQL 데이터 적재 결과 검증 스크립트 (se 포함)
# ==========================================================

import urllib.parse
# 1. SQL 조회 결과를 표 형태로 받아오기 위한 pandas 라이브러리 로드[cite: 4]
import pandas as pd
# 2. 파이썬과 MySQL을 연결해주는 SQLAlchemy 엔진 생성 함수 로드[cite: 4]
from sqlalchemy import create_engine

# 3. MySQL 접속 주소 설정[cite: 4]
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "shelter_project"

encoded_pw = urllib.parse.quote_plus(DB_PASSWORD)
DB_URL = f"mysql+pymysql://{DB_USER}:{encoded_pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def verify_database():
    try:
        # 4. DB 연결 통로(엔진) 생성[cite: 4]
        engine = create_engine(DB_URL)
        
        # 5. DB의 flood_shelter 테이블에 저장된 전체 행 개수 확인[cite: 4]
        count_query = "SELECT COUNT(*) AS total_count FROM flood_shelter"
        count_df = pd.read_sql(count_query, con=engine)
        total_count = count_df['total_count'].iloc[0]
        
        print("=" * 75)
        print(f"🎉 [DB 검증 완료] flood_shelter 테이블에 총 {total_count:,}건의 데이터가 저장되어 있습니다!")
        print("-" * 75)
        
        # 6. 🌟 [수정 완료] shlt_id와 se 컬럼을 포함한 상위 3건 샘플 데이터 조회
        sample_query = """
            SELECT shlt_id, ctpv_nm, sgg_nm, fclt_nm, daddr, lot, lat, se 
            FROM flood_shelter 
            LIMIT 3
        """
        sample_df = pd.read_sql(sample_query, con=engine)
        print("📋 [저장된 데이터 샘플 3건 (shlt_id 및 se 구분코드 확인)]:")
        print(sample_df)
        print("=" * 75)

    except Exception as e:
        # 7. DB 접속 실패 시 에러 출력[cite: 4]
        print(f"❌ DB 접속 및 조회 실패: {e}")

if __name__ == "__main__":
    verify_database()
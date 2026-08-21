import urllib.parse
import pandas as pd
from sqlalchemy import create_engine

# 1. DB 접속 정보 설정
DB_USER = "root"
DB_PASSWORD = "root"  # 본인의 비밀번호로 변경하세요
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "shelter_db"

encoded_pw = urllib.parse.quote_plus(DB_PASSWORD)
DB_URL = f"mysql+pymysql://{DB_USER}:{encoded_pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def check_db():
    engine = create_engine(DB_URL)
    tables = ['earthquake', 'airstrike', 'flood']
    
    print("=" * 70)
    print("🔍 [DB 통합 검증] 3개 테이블 상태 확인 시작")
    print("=" * 70)
    
    for table in tables:
        try:
            # 2. 데이터 건수 확인
            count_df = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", con=engine)
            count = count_df['cnt'].iloc[0]
            
            # 3. 데이터 샘플 조회 (최근 1건)
            sample_df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", con=engine)
            
            print(f"✅ 테이블명: {table.upper()}")
            print(f"   - 총 데이터 수: {count:,}건")
            print(f"   - 샘플 데이터 (se, mng_dept_nm 확인):")
            print(sample_df[['se', 'mng_dept_nm']])
            print("-" * 70)
            
        except Exception as e:
            print(f"❌ {table} 테이블 조회 실패: {e}")
            print("-" * 70)

    print("🎉 모든 테이블 검증 완료!")

if __name__ == "__main__":
    check_db()
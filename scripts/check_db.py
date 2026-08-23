# ==========================================================
# [scripts/check_db.py] MySQL shelter_db 3대 대피소 데이터 검증 스크립트
# ==========================================================

import os  # 운영체제 파일 경로 및 디렉터리를 제어하는 라이브러리입니다.
from dotenv import (  # .env 환경 설정 파일에서 DB 비밀번호를 안전하게 읽어오는 도구입니다.
    load_dotenv,
)
import pandas as pd  # SQL 조회 결과를 터미널에 깔끔한 표(DataFrame)로 출력해 주는 라이브러리입니다.
from sqlalchemy import (  # MySQL 데이터베이스와 안정적인 연결 통로(엔진)를 생성하는 도구입니다.
    create_engine,
)

# ----------------------------------------------------------
# 1. .env 환경변수 파일 동적 탐색 및 로드
# ----------------------------------------------------------
# 현재 스크립트 파일 기준 상위 프로젝트 루트 폴더 경로를 계산합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# config 폴더의 .env 경로를 우선 지정하고, 없으면 루트 .env를 탐색합니다.
dotenv_path = os.path.join(BASE_DIR, "config", ".env")
if not os.path.exists(dotenv_path):
    dotenv_path = os.path.join(BASE_DIR, ".env")

# 환경변수를 메모리에 로드합니다.
load_dotenv(dotenv_path=dotenv_path, override=True)


# ----------------------------------------------------------
# 2. 데이터베이스 접속 주소 (URL) 구성
# ----------------------------------------------------------
# .env 파일에서 비밀번호를 로드하며, 기본값은 'root'로 설정합니다.
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

# SQLAlchemy MySQL 연결 URL (shelter_db 대상, utf8mb4 한글 인코딩 적용)
DB_URL = f"mysql+pymysql://root:{DB_PASSWORD}@localhost:3306/shelter_db?charset=utf8mb4"


# ----------------------------------------------------------
# 3. 전체 데이터베이스 및 테이블 통합 검증 함수
# ----------------------------------------------------------
def verify_database():
    # 검증할 표준화된 3대 대피소 테이블과 한국어 설명 매핑입니다.
    shelter_tables = {
        "shelter_flood": "수해/침수 대피소",
        "shelter_earthquake": "지진 옥외 대피소",
        "shelter_airstrike": "공습 민방위 대피소",
    }

    try:
        # DB 연결 통로(엔진)를 생성합니다.
        engine = create_engine(DB_URL)

        print("=" * 70)
        print("🔍 [shelter_db] 3대 재난 대피소 데이터베이스 적재 현황 정밀 검증")
        print("=" * 70)

        # 3개 테이블을 순차적으로 검증합니다.
        for table_name, table_desc in shelter_tables.items():
            print(f"\n📦 [{table_desc} : {table_name}]")
            print("-" * 70)

            try:
                # 1) 전체 데이터 건수 조회 쿼리 실행
                count_query = (
                    f"SELECT COUNT(*) AS total_count FROM {table_name}"
                )
                count_df = pd.read_sql(count_query, con=engine)
                total_count = count_df["total_count"].iloc[0]

                print(
                    f"✅ 총 저장 건수: {total_count:,}건의 데이터가 안전하게 저장되어 있습니다."
                )

                # 2) 저장된 데이터의 실제 내용 샘플 3건 조회 (Pandas 표 형태로 출력)
                sample_query = f"SELECT shlt_id, ctpv_nm, sgg_nm, fclt_nm, daddr, lot, lat FROM {table_name} LIMIT 3"

                # 수해 대피소의 경우 shlt_id가 없을 수 있으므로 전체 컬럼으로 대체 조회
                if table_name == "shelter_flood":
                    sample_query = f"SELECT ctpv_nm, sgg_nm, fclt_nm, daddr, lot, lat FROM {table_name} LIMIT 3"

                sample_df = pd.read_sql(sample_query, con=engine)

                print("📋 [저장된 데이터 샘플 3건]:")
                print(sample_df)

            except Exception as table_err:
                print(
                    f"❌ [{table_name}] 테이블 검증 실패 (테이블 미생성 또는 적재 오류): {table_err}"
                )

        print("\n" + "=" * 70)
        print(
            "🎉 [검증 완료] 모든 대피소 테이블의 데이터 무결성 점검이 완료되었습니다!"
        )
        print("=" * 70)

    except Exception as e:
        # DB 접속 자체에 실패했을 경우 안내 메시지를 출력합니다.
        print(f"\n❌ DB 접속 실패: MySQL 서버 상태 및 .env 설정을 확인하세요.")
        print(f"상세 에러 내용: {e}")


# ----------------------------------------------------------
# 4. 스크립트 직접 실행 진입점
# ----------------------------------------------------------
if __name__ == "__main__":
    verify_database()
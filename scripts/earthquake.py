import math  # 페이징 계산 라이브러리
import os  # 디렉터리 경로 제어 라이브러리
from dotenv import load_dotenv  # 환경변수 로드 라이브러리
import pymysql  # MySQL 통신 드라이버
import requests  # 공공 API HTTP 통신 라이브러리

# 프로젝트 루트 경로 계산 및 .env 로드
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, "config", ".env")

if not os.path.exists(dotenv_path):
    dotenv_path = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=dotenv_path, override=True)

# 환경변수 검증
EARTHQUAKE_API_KEY = os.getenv("EARTHQUAKE_API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

if not EARTHQUAKE_API_KEY:
    print("❌ EARTHQUAKE_API_KEY를 읽지 못했습니다. .env 파일을 확인해 주세요.")
    exit()

# 서울시 지진옥외대피장소 API 엔드포인트
BASE_URL = (
    f"http://openapi.seoul.go.kr:8088/{EARTHQUAKE_API_KEY}/json/TbEqkShelter"
)

# MySQL 데이터베이스 접속 설정
db_config = {
    "host": "localhost",
    "user": "root",
    "password": DB_PASSWORD,
    "database": "shelter_db",
    "charset": "utf8mb4",
}


def fetch_and_save_data():
    connection = None

    try:
        print("\n[1] 지진대피소 전체 데이터 개수 확인 중...")
        response = requests.get(f"{BASE_URL}/1/1/", timeout=30)
        response.raise_for_status()

        data = response.json()
        total_count = data["TbEqkShelter"]["list_total_count"]
        print(f"지진대피소 총 데이터 개수: {total_count}개")

        page_size = 1000
        total_pages = math.ceil(total_count / page_size)
        print(f"총 {total_pages}번 분할 요청합니다.")

        print("\n[2] MySQL 연결 중...")
        connection = pymysql.connect(**db_config)
        print("✅ MySQL 연결 성공")

        with connection.cursor() as cursor:
            # shelter_earthquake 테이블 자동 생성 (DDL)
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS shelter_earthquake (
                    shlt_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '대피소 고유 번호',
                    ctpv_nm VARCHAR(50) COMMENT '시도명',
                    sgg_nm VARCHAR(50) COMMENT '시군구명',
                    fclt_nm VARCHAR(200) NOT NULL COMMENT '대피소 시설명',
                    daddr VARCHAR(300) COMMENT '도로명 상세주소',
                    lot DOUBLE COMMENT '경도 좌표',
                    lat DOUBLE COMMENT '위도 좌표',
                    mng_dept_nm VARCHAR(100) COMMENT '담당 관리부서',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '수집 일시'
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(create_table_sql)
            print("✅ shelter_earthquake 테이블 점검 및 준비 완료")

            # 기존 데이터 초기화 (TRUNCATE)
            cursor.execute("TRUNCATE TABLE shelter_earthquake")
            print("✅ 기존 데이터 초기화 완료")

            # INSERT SQL 템플릿
            sql = """
                INSERT INTO shelter_earthquake
                (ctpv_nm, sgg_nm, fclt_nm, daddr, lot, lat, mng_dept_nm)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # 페이징 수집 및 적재
            for i in range(total_pages):
                start = (i * page_size) + 1
                end = min((i + 1) * page_size, total_count)
                print(f"[{i + 1}/{total_pages}] {start} ~ {end} 요청 및 적재 중...")

                url = f"{BASE_URL}/{start}/{end}/"
                res = requests.get(url, timeout=30)
                res.raise_for_status()

                batch_data = res.json()
                rows = batch_data["TbEqkShelter"].get("row", [])

                for row in rows:
                    values = (
                        row.get("CTPV_NM"),
                        row.get("SGG_NM"),
                        row.get("FCLT_NM"),
                        row.get("DADDR"),
                        row.get("LOT"),
                        row.get("LAT"),
                        row.get("MNG_DEPT_NM"),
                    )
                    cursor.execute(sql, values)

        connection.commit()
        print("\n========================================")
        print("🎉 지진대피소 전체 데이터 저장 완료!")
        print("========================================")

        # 저장 결과 검증
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM shelter_earthquake")
            saved_count = cursor.fetchone()[0]
            print(f"📊 DB 실제 저장 개수: {saved_count}개")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        if connection:
            connection.rollback()
            print("↩️ ROLLBACK 완료")

    finally:
        if connection:
            connection.close()
            print("🔒 MySQL 연결 종료")


if __name__ == "__main__":
    fetch_and_save_data()
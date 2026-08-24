import os
import math
import pymysql
import requests
from dotenv import load_dotenv


# ============================================================
# 1. .env 경로 설정
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

dotenv_path = os.path.join(
    BASE_DIR,
    "config",
    ".env"
)

load_dotenv(
    dotenv_path=dotenv_path,
    override=True
)


# ============================================================
# 2. 환경변수 읽기
# ============================================================

EARTHQUAKE_API_KEY = os.getenv(
    "EARTHQUAKE_API_KEY"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD"
)


if not EARTHQUAKE_API_KEY:
    print(
        "❌ EARTHQUAKE_API_KEY를 읽지 못했습니다."
    )
    exit()


if not DB_PASSWORD:
    print(
        "❌ DB_PASSWORD를 읽지 못했습니다."
    )
    exit()


print("✅ 지진대피소 API 인증키 읽기 완료")
print("✅ DB 비밀번호 읽기 완료")


# ============================================================
# 3. 서울 지진대피소 API
# ============================================================

BASE_URL = (
    f"http://openapi.seoul.go.kr:8088/"
    f"{EARTHQUAKE_API_KEY}/json/TbEqkShelter"
)


# ============================================================
# 4. MySQL 접속 정보 (shelter_db 사용)
# ============================================================

db_config = {
    "host": "localhost",
    "user": "root",
    "password": DB_PASSWORD,
    "database": "shelter_db",
    "charset": "utf8mb4"
}


# ============================================================
# 5. 데이터 수집
# ============================================================

def fetch_and_save_data():

    connection = None

    try:

        # ----------------------------------------------------
        # 전체 데이터 개수 확인
        # ----------------------------------------------------

        print("\n[1] 지진대피소 전체 데이터 개수 확인 중...")

        response = requests.get(
            f"{BASE_URL}/1/1/",
            timeout=30
        )

        print(
            f"서버 응답 상태 코드: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        data = response.json()

        api_data = data["TbEqkShelter"]

        total_count = api_data["list_total_count"]

        print(
            f"지진대피소 총 데이터 개수: "
            f"{total_count}개"
        )


        # ----------------------------------------------------
        # 1000개씩 처리
        # ----------------------------------------------------

        page_size = 1000

        total_pages = math.ceil(
            total_count / page_size
        )

        print(
            f"총 {total_pages}번 요청합니다."
        )


        # ----------------------------------------------------
        # MySQL 연결
        # ----------------------------------------------------

        print("\n[2] MySQL 연결 중...")

        connection = pymysql.connect(
            **db_config
        )

        print("✅ MySQL 연결 성공")


        with connection.cursor() as cursor:

            # ------------------------------------------------
            # 기존 데이터 삭제 (earthquake 테이블)
            # ------------------------------------------------

            print("\n[3] 기존 지진대피소 데이터 삭제 중...")

            cursor.execute(
                "TRUNCATE TABLE earthquake"
            )

            print("✅ 기존 데이터 삭제 완료")


            # ------------------------------------------------
            # INSERT SQL (shlt_id, se 칼럼 추가 반영)
            # ------------------------------------------------

            sql = """
                  INSERT INTO earthquake
                  (
                      shlt_id,
                      ctpv_nm,
                      sgg_nm,
                      fclt_nm,
                      daddr,
                      lot,
                      lat,
                      mng_dept_nm,
                      se
                  )
                  VALUES
                      (
                          %s,
                          %s,
                          %s,
                          %s,
                          %s,
                          %s,
                          %s,
                          %s,
                          %s
                      ) \
                  """


            # ------------------------------------------------
            # 1000개씩 요청
            # ------------------------------------------------

            for i in range(total_pages):

                start = (
                                i * page_size
                        ) + 1

                end = min(
                    (i + 1) * page_size,
                    total_count
                )

                print(
                    f"\n[{i + 1}/{total_pages}] "
                    f"{start} ~ {end} 요청 중..."
                )


                url = (
                    f"{BASE_URL}/"
                    f"{start}/"
                    f"{end}/"
                )


                response = requests.get(
                    url,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                rows = data[
                    "TbEqkShelter"
                ].get("row", [])


                print(
                    f"가져온 데이터: "
                    f"{len(rows)}개"
                )


                # ------------------------------------------------
                # DB 저장 (SHLT_id 및 SE 데이터 매핑)
                # ------------------------------------------------

                for row in rows:

                    values = (
                        row.get("SHLT_id"),     # 피난처 ID
                        row.get("CTPV_NM"),     # 시도명
                        row.get("SGG_NM"),      # 시군구명
                        row.get("FCLT_NM"),     # 시설명
                        row.get("DADDR"),       # 상세주소
                        row.get("LOT"),         # 경도
                        row.get("LAT"),         # 위도
                        row.get("MNG_DEPT_NM"), # 관리부서
                        row.get("SE")           # 구분 칼럼 (API 데이터)
                    )


                    cursor.execute(
                        sql,
                        values
                    )


                print(
                    f"✅ {start} ~ {end} "
                    f"저장 완료!"
                )


        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------

        connection.commit()

        print("\n========================================")
        print("🎉 지진대피소 전체 데이터 저장 완료!")
        print("========================================")


        # ----------------------------------------------------
        # 저장 개수 확인
        # ----------------------------------------------------

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT COUNT(*) "
                "FROM earthquake"
            )

            saved_count = cursor.fetchone()[0]

            print(
                f"DB 실제 저장 개수: "
                f"{saved_count}개"
            )


            # ------------------------------------------------
            # 데이터 확인
            # ------------------------------------------------

            cursor.execute("""
                           SELECT *
                           FROM earthquake
                           LIMIT 5
                           """)

            result = cursor.fetchall()

            print("\n[저장된 데이터 확인]")

            for row in result:
                print(row)


    except Exception as e:

        print("\n❌ 오류 발생!")
        print(e)

        if connection:
            connection.rollback()

            print("↩️ ROLLBACK 완료")


    finally:

        if connection:
            connection.close()

            print("\nMySQL 연결 종료")


# ============================================================
# 6. 실행
# ============================================================

if __name__ == "__main__":
    fetch_and_save_data()
import os
import math
import re  # 정규식 사용을 위한 모듈 추가
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

API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")


if not API_KEY:
    print("❌ API_KEY를 읽지 못했습니다.")
    exit()

if not DB_PASSWORD:
    print("❌ DB_PASSWORD를 읽지 못했습니다.")
    exit()


print("✅ 공습대피소 API 인증키 읽기 완료")
print("✅ DB 비밀번호 읽기 완료")


# ============================================================
# 3. 서울 공습대피소 API
# ============================================================

BASE_URL = (
    f"http://openapi.seoul.go.kr:8088/"
    f"{API_KEY}/json/LOCALDATA_114602"
)


# ============================================================
# 4. MySQL 접속 정보
# ============================================================

db_config = {
    "host": "localhost",
    "user": "root",
    "password": DB_PASSWORD,
    "database": "airstrike",
    "charset": "utf8mb4"
}


# ============================================================
# 5. 데이터 수집 함수
# ============================================================

def fetch_and_save_data():

    connection = None

    try:

        # ----------------------------------------------------
        # 전체 데이터 개수 확인
        # ----------------------------------------------------

        print("\n[1] 공습대피소 전체 데이터 개수 확인 중...")

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

        api_data = data["LOCALDATA_114602"]

        total_count = api_data["list_total_count"]

        print(
            f"공습대피소 총 데이터 개수: "
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
            # 기존 데이터 삭제
            # ------------------------------------------------

            print("\n[3] 기존 공습대피소 데이터 삭제 중...")

            cursor.execute(
                "TRUNCATE TABLE air_shelter_info"
            )

            print("✅ 기존 데이터 삭제 완료")


            # ------------------------------------------------
            # INSERT SQL
            # ------------------------------------------------

            sql = """
                  INSERT INTO air_shelter_info
                  (
                      ctpv_nm,
                      sgg_nm,
                      fclt_nm,
                      daddr,
                      lot,
                      lat,
                      mng_dept_nm
                  )
                  VALUES
                      (
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
                    "LOCALDATA_114602"
                ].get("row", [])


                print(
                    f"가져온 데이터: "
                    f"{len(rows)}개"
                )


                # ------------------------------------------------
                # DB 저장 (주소 기반 구 이름 추출 로직 포함)
                # ------------------------------------------------

                for row in rows:

                    # 좌표 변환 예외 처리
                    try:
                        longitude = float(
                            row.get("XCRD") or 0
                        )
                    except (ValueError, TypeError):
                        longitude = 0.0

                    try:
                        latitude = float(
                            row.get("YCRD") or 0
                        )
                    except (ValueError, TypeError):
                        latitude = 0.0


                    # 1. ctpv_nm은 무조건 '서울특별시'로 고정
                    ctpv_nm = "서울특별시"


                    # 2. 주소(LOTNO_ADDR)에서 'OO구' 패턴을 찾아 sgg_nm 추출
                    address = row.get("LOTNO_ADDR") or ""
                    sgg_nm = "-"

                    # 정규식을 이용해 'OO구' (예: 강동구, 종로구 등) 추출
                    match = re.search(r'([가-힣]+구)', address)
                    if match:
                        sgg_nm = match.group(1)


                    values = (
                        ctpv_nm,
                        sgg_nm,
                        row.get("BPLC_NM"),
                        address,
                        longitude,
                        latitude,
                        row.get("MNG_DEPT_NM") or "-"
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
        print("🎉 공습대피소 전체 데이터 저장 완료!")
        print("========================================")


        # ----------------------------------------------------
        # 저장 개수 확인
        # ----------------------------------------------------

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT COUNT(*) "
                "FROM air_shelter_info"
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
                           SELECT
                               shlt_id,
                               ctpv_nm,
                               sgg_nm,
                               fclt_nm,
                               daddr,
                               lot,
                               lat,
                               mng_dept_nm
                           FROM air_shelter_info
                           ORDER BY shlt_id
                           LIMIT 5
                           """)

            result = cursor.fetchall()

            print("\n[shlt_id 확인]")

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
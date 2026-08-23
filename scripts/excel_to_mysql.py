# <<<<<<< HEAD
# # 20260820 12:00
# =======
# >>>>>>> cb7f219db7d045772f6cc5dc51e1d158b1cd3de4
# ==========================================================
# [scripts/excel_to_mysql.py]
# 엑셀 데이터 -> MySQL flood_shelter (표준 컬럼) 일괄 적재
# ==========================================================

import os  # 운영체제 파일 및 디렉터리 경로 제어 라이브러리
import pandas as pd  # 대용량 표 데이터 처리 및 정제 라이브러리
from sqlalchemy import (  # MySQL 커넥션 엔진 생성 모듈
    create_engine,
)

# 현재 스크립트가 위치한 scripts 폴더의 절대 경로를 계산합니다.
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# shelter_db 데이터베이스 연결 주소 (한글 인코딩 utf8mb4 적용)
DB_URL = "mysql+pymysql://root:root@localhost:3306/shelter_db?charset=utf8mb4"


def run_etl():
    print("=" * 60)
    print("🚀 [수해 대피소] 엑셀 데이터 적재 시작")
    print("=" * 60)

    # scripts 폴더 안에서 flood_shelter 엑셀 파일을 탐색합니다.
    target_file = None
    for f in os.listdir(FOLDER_PATH):
        if f.startswith("flood_shelter") and (
            f.endswith(".xlsx") or f.endswith(".xls")
        ):
            target_file = os.path.join(FOLDER_PATH, f)
            break

    if not target_file:
        print(f"❌ flood_shelter 엑셀 파일을 찾을 수 없습니다: {FOLDER_PATH}")
        return

    # 엑셀 파일 로드
    raw_df = pd.read_excel(target_file, engine="openpyxl")
    print(f"📄 원본 엑셀 데이터 {len(raw_df):,}건 로드 완료")

    print("\n🧹 MySQL 테이블 규격에 맞춰 컬럼 데이터 정제 중...")
    clean_df = pd.DataFrame()

    # 표준 컬럼 매핑
    clean_df["ctpv_nm"] = raw_df["ctpv_nm"].astype(str)
    clean_df["sgg_nm"] = raw_df["sgg_nm"].astype(str)
    clean_df["fclt_nm"] = raw_df["fclt_nm"].astype(str)
    clean_df["daddr"] = raw_df["daddr"].astype(str)
    clean_df["lot"] = pd.to_numeric(raw_df["lot"], errors="coerce")
    clean_df["lat"] = pd.to_numeric(raw_df["lat"], errors="coerce")
    clean_df["mng_dept_nm"] = raw_df["mng_dept_nm"].fillna("미지정")

    # 필수 데이터 결측치 행 제거
    clean_df = clean_df.dropna(subset=["lat", "lot", "fclt_nm"])
    print(f"✨ 정제 완료: 유효 데이터 {len(clean_df):,}건 준비됨")

    print("\n💾 MySQL shelter_flood 테이블에 적재 중...")
    engine = create_engine(DB_URL)

    # shelter_flood 테이블로 데이터 적재
    clean_df.to_sql(name="shelter_flood", con=engine, if_exists="replace", index=False)

    print("=" * 60)
    print(
        f"🎉 [완료] 총 {len(clean_df):,}건이 'shelter_flood' 테이블에 성공적으로 저장되었습니다!"
    )
    print("=" * 60)


if __name__ == "__main__":
    run_etl()
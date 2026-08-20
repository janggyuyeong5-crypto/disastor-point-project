# 20260820 12:00
# scripts/check_excel.py
import pandas as pd

# 엑셀 파일 경로
EXCEL_PATH = "scripts/flood_shelter.xlsx"

try:
    # 엑셀 읽기
    df = pd.read_excel(EXCEL_PATH, engine='openpyxl')
    print("=" * 60)
    print(f"✅ 엑셀 로드 성공! 총 {len(df):,}개의 데이터가 있습니다.")
    print("-" * 60)
    print("📋 [포함된 컬럼(열) 이름 목록]:")
    for idx, col in enumerate(df.columns, 1):
        print(f"  {idx}. {col}")
    print("=" * 60)
except Exception as e:
    print(f"❌ 에러 발생: {e}")
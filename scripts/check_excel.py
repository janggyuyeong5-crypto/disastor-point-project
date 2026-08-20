# ==========================================================
# [scripts/check_excel.py] 엑셀 파일 컬럼 및 se 데이터 사전 점검 스크립트
# ==========================================================

import pandas as pd

EXCEL_PATH = "scripts/flood_shelter.xlsx"

try:
    # 엑셀 읽기[cite: 5]
    df = pd.read_excel(EXCEL_PATH, engine='openpyxl')
    print("=" * 65)
    print(f"✅ 엑셀 로드 성공! 총 {len(df):,}개의 행 데이터가 있습니다.")
    print("-" * 65)
    print("📋 [포함된 컬럼(열) 이름 목록]:")
    for idx, col in enumerate(df.columns, 1):
        print(f"  {idx}. {col}")
    print("-" * 65)
    
    # se 컬럼 존재 여부 및 값 분포 확인
    if 'se' in df.columns:
        print(f"🌟 [se 컬럼 데이터 확인]: {df['se'].unique().tolist()} (총 {len(df['se'])}건)")
    print("=" * 65)
except Exception as e:
    print(f"❌ 에러 발생: {e}")
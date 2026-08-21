import os
import pandas as pd

FOLDER_PATH = "scripts"

def check_excel():
    print("=" * 70)
    print("🔍 [엑셀 통합 검증] 파일 및 데이터 구조 확인")
    print("=" * 70)

    # scripts 폴더 내의 모든 엑셀 파일 탐색
    excel_files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(('.xlsx', '.xls'))]
    
    if not excel_files:
        print("❌ scripts 폴더 내에 엑셀 파일을 찾을 수 없습니다.")
        return

    for file in excel_files:
        file_path = os.path.join(FOLDER_PATH, file)
        try:
            # 엑셀 파일 로드 (openpyxl 엔진 사용)
            df = pd.read_excel(file_path, engine='openpyxl')
            
            print(f"✅ 파일명: {file}")
            print(f"   - 총 데이터 수: {len(df):,}건")
            print(f"   - 컬럼 목록: {', '.join(df.columns.tolist())}")
            
            # 홍수대피소 파일인 경우 특정 컬럼 샘플 확인
            if 'flood_shelter' in file:
                print(f"   - 샘플 데이터 (상위 1건):")
                print(df.head(1).to_string(index=False))
            
            print("-" * 70)
            
        except Exception as e:
            print(f"❌ {file} 파일 읽기 실패: {e}")
            print("-" * 70)

    print("🎉 엑셀 파일 검증 완료!")

if __name__ == "__main__":
    check_excel()
import pandas as pd

CSV_FILE = "OBS_ASOS_DD_20260922162003.csv"

df = pd.read_csv(CSV_FILE, encoding="cp949")

print("데이터 개수:", len(df))
print()
print("컬럼:")
print(df.columns.tolist())
print()
print("처음 5개 데이터:")
print(df.head())
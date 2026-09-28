import os

import firebase_admin
import pandas as pd
from dotenv import load_dotenv
from firebase_admin import credentials, firestore


load_dotenv()


# Firebase 연결
firebase_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

if not firebase_key_path:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON 환경변수가 설정되지 않았습니다.")

cred = credentials.Certificate(firebase_key_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# CSV 읽기
CSV_FILE = "OBS_ASOS_DD_20260922162003.csv"

df = pd.read_csv(CSV_FILE, encoding="cp949")


# Firestore에 데이터 저장
collection_ref = db.collection("data")

for _, row in df.iterrows():
    data = {
        "date": str(row["일시"]),
        "value": float(row["평균기온(°C)"]),
        "memo": "대전 일평균 기온"
    }

    collection_ref.add(data)


print(f"{len(df)}개의 데이터를 Firestore에 저장했습니다.")
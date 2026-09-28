import os

import firebase_admin
from dotenv import load_dotenv
from fastapi import FastAPI
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from openai import OpenAI


load_dotenv()

app = FastAPI()

openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase 연결
firebase_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

if not firebase_key_path:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON 환경변수가 설정되지 않았습니다.")

cred = credentials.Certificate(firebase_key_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# 데이터 요청 형식
class DataCreate(BaseModel):
    date: str
    value: float
    memo: str = ""

class Message(BaseModel):
    role: str
    content: str


class ConversationCreate(BaseModel):
    title: str
    messages: list[Message]

# 기본 확인
@app.get("/")
def root():
    return {"message": "AI Assistant API is running!"}


# 데이터 목록 조회
@app.get("/api/data")
def get_data():
    docs = db.collection("data").stream()

    result = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        result.append(data)

    return result

# 데이터 추가
@app.post("/api/data")
def create_data(data: DataCreate):
    doc_ref = db.collection("data").document()

    doc_ref.set({
        "date": data.date,
        "value": data.value,
        "memo": data.memo
    })

    return {
        "id": doc_ref.id,
        "date": data.date,
        "value": data.value,
        "memo": data.memo
    }

# 데이터 수정
@app.put("/api/data/{data_id}")
def update_data(data_id: str, data: DataCreate):
    doc_ref = db.collection("data").document(data_id)

    if not doc_ref.get().exists:
        return {"error": "데이터를 찾을 수 없습니다."}

    doc_ref.update({
        "date": data.date,
        "value": data.value,
        "memo": data.memo
    })

    return {
        "id": data_id,
        "date": data.date,
        "value": data.value,
        "memo": data.memo
    }

# 데이터 삭제
@app.delete("/api/data/{data_id}")
def delete_data(data_id: str):
    doc_ref = db.collection("data").document(data_id)

    if not doc_ref.get().exists:
        return {"error": "데이터를 찾을 수 없습니다."}

    doc_ref.delete()

    return {
        "message": "데이터가 삭제되었습니다.",
        "id": data_id
    }

# 데이터 요약
@app.get("/api/data/summary")
def get_data_summary():
    docs = db.collection("data").stream()

    data_list = []

    for doc in docs:
        data = doc.to_dict()
        data_list.append(data)

    if not data_list:
        return {
            "period": None,
            "count": 0,
            "metrics": {
                "average": None,
                "max": None,
                "min": None
            },
            "trend": "데이터 없음"
        }

    values = [float(item["value"]) for item in data_list]

    dates = sorted(item["date"] for item in data_list)

    average = sum(values) / len(values)
    maximum = max(values)
    minimum = min(values)

    # 최근 추세 계산
    sorted_data = sorted(data_list, key=lambda x: x["date"])

    if len(sorted_data) >= 14:
        recent_values = [
            float(item["value"])
            for item in sorted_data[-7:]
        ]

        previous_values = [
            float(item["value"])
            for item in sorted_data[-14:-7]
        ]

        recent_average = sum(recent_values) / len(recent_values)
        previous_average = sum(previous_values) / len(previous_values)

        difference = recent_average - previous_average

        if difference > 0.5:
            trend = "상승"
        elif difference < -0.5:
            trend = "하락"
        else:
            trend = "유지"
    else:
        trend = "데이터 부족"

    return {
        "period": f"{dates[0]} ~ {dates[-1]}",
        "count": len(data_list),
        "metrics": {
            "average": round(average, 2),
            "max": maximum,
            "min": minimum
        },
        "trend": trend
    }

# 대화 저장
@app.post("/api/conversations")
def create_conversation(conversation: ConversationCreate):
    doc_ref = db.collection("conversations").document()

    messages = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in conversation.messages
    ]

    doc_ref.set({
        "title": conversation.title,
        "messages": messages
    })

    return {
        "id": doc_ref.id,
        "title": conversation.title,
        "messages": messages
    }

# 대화 목록 조회
@app.get("/api/conversations")
def get_conversations():
    docs = db.collection("conversations").stream()

    result = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        result.append(data)

    return result

# 특정 대화 조회
@app.get("/api/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    doc_ref = db.collection("conversations").document(conversation_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": "대화를 찾을 수 없습니다."}

    data = doc.to_dict()
    data["id"] = doc.id

    return data

# 대화 삭제
@app.delete("/api/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    doc_ref = db.collection("conversations").document(conversation_id)

    if not doc_ref.get().exists:
        return {"error": "대화를 찾을 수 없습니다."}

    doc_ref.delete()

    return {
        "message": "대화가 삭제되었습니다.",
        "id": conversation_id
    }

# 채팅 요청 형식
class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


# AI 채팅
@app.post("/api/chat")
def chat(request: ChatRequest):
    # 1. Firestore에서 데이터 가져오기
    docs = db.collection("data").stream()

    data_list = []

    for doc in docs:
        data = doc.to_dict()
        data_list.append(data)

    # 2. 데이터 요약
    if not data_list:
        summary = {
            "period": None,
            "count": 0,
            "metrics": {
                "average": None,
                "max": None,
                "min": None
            },
            "trend": "데이터 없음"
        }
    else:
        values = [float(item["value"]) for item in data_list]
        dates = sorted(item["date"] for item in data_list)

        average = sum(values) / len(values)
        maximum = max(values)
        minimum = min(values)

        sorted_data = sorted(data_list, key=lambda x: x["date"])

        if len(sorted_data) >= 14:
            recent_values = [
                float(item["value"])
                for item in sorted_data[-7:]
            ]

            previous_values = [
                float(item["value"])
                for item in sorted_data[-14:-7]
            ]

            recent_average = sum(recent_values) / len(recent_values)
            previous_average = sum(previous_values) / len(previous_values)

            difference = recent_average - previous_average

            if difference > 0.5:
                trend = "상승"
            elif difference < -0.5:
                trend = "하락"
            else:
                trend = "유지"
        else:
            trend = "데이터 부족"

        summary = {
            "period": f"{dates[0]} ~ {dates[-1]}",
            "count": len(data_list),
            "metrics": {
                "average": round(average, 2),
                "max": maximum,
                "min": minimum
            },
            "trend": trend
        }

    # 3. 기존 대화 불러오기
    conversation_messages = []

    if request.conversation_id:
        conversation_ref = db.collection("conversations").document(
            request.conversation_id
        )
        conversation_doc = conversation_ref.get()

        if conversation_doc.exists:
            conversation_data = conversation_doc.to_dict()

            conversation_messages = conversation_data.get(
                "messages",
                []
            )

    # 4. system prompt
    system_prompt = f"""
너는 사용자의 데이터를 분석하고 질문에 답하는 AI 비서다.

현재 저장된 데이터의 요약 정보는 다음과 같다.

{summary}

이 요약 정보를 참고하여 사용자의 질문에 답변하라.
데이터에 없는 내용은 추측하지 말고, 알 수 없다고 답변하라.
이전 대화 내용이 제공되었다면 그 맥락을 참고하여 자연스럽게 답변하라.
"""

    # 5. GPT에 전달할 메시지 구성
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for message in conversation_messages:
        messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    messages.append({
        "role": "user",
        "content": request.message
    })

    # 6. OpenAI API 호출
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    # 7. 대화 저장
    if request.conversation_id:
        conversation_ref = db.collection("conversations").document(
            request.conversation_id
        )

        updated_messages = conversation_messages + [
            {
                "role": "user",
                "content": request.message
            },
            {
                "role": "assistant",
                "content": answer
            }
        ]

        conversation_ref.update({
            "messages": updated_messages
        })

        conversation_id = request.conversation_id

    else:
        doc_ref = db.collection("conversations").document()

        messages_to_save = [
            {
                "role": "user",
                "content": request.message
            },
            {
                "role": "assistant",
                "content": answer
            }
        ]

        doc_ref.set({
            "title": request.message[:30],
            "messages": messages_to_save
        })

        conversation_id = doc_ref.id

    # 8. 결과 반환
    return {
        "answer": answer,
        "conversation_id": conversation_id,
        "summary": summary
    }
import json
import os

import firebase_admin
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, firestore
from openai import OpenAI
from pydantic import BaseModel, Field

from routers.data import router as data_router
from routers.conversations import router as conversations_router
from services.summary_service import get_summary
from services.ai_service import chat_with_ai


load_dotenv()


# ==============================
# FastAPI 앱
# ==============================

app = FastAPI()


# ==============================
# CORS 설정
# ==============================

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


# ==============================
# OpenAI 연결
# ==============================

openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ==============================
# Firebase 연결
# ==============================

firebase_service_account = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_JSON"
)

if not firebase_service_account:
    raise ValueError(
        "FIREBASE_SERVICE_ACCOUNT_JSON 환경변수가 설정되지 않았습니다."
    )

try:
    if firebase_service_account.strip().startswith("{"):
        service_account_info = json.loads(
            firebase_service_account
        )
        cred = credentials.Certificate(
            service_account_info
        )
    else:
        cred = credentials.Certificate(
            firebase_service_account
        )

except (json.JSONDecodeError, ValueError) as error:
    raise ValueError(
        "FIREBASE_SERVICE_ACCOUNT_JSON 형식이 올바르지 않습니다."
    ) from error

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ==============================
# Router 연결
# ==============================

app.include_router(data_router)
app.include_router(conversations_router)


# ==============================
# AI 채팅 관련 모델
# ==============================

class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000
    )

    conversation_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
    summary: dict


class SummaryMetrics(BaseModel):
    average: float | None
    max: float | None
    min: float | None


class SummaryResponse(BaseModel):
    period: str | None
    count: int
    metrics: SummaryMetrics
    trend: str


# ==============================
# 기본 확인
# ==============================

@app.get("/")
def root():
    return {
        "message": "AI Assistant API is running!"
    }


# ==============================
# 데이터 요약
# ==============================

@app.get(
    "/api/data/summary",
    response_model=SummaryResponse
)
def get_data_summary():
    return get_summary(db)


# ==============================
# AI 채팅
# ==============================

@app.post(
    "/api/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # 데이터 요약
    summary = get_summary(db)

    # AI 서비스 호출
    result = chat_with_ai(
        openai=openai,
        db=db,
        message=request.message,
        conversation_id=request.conversation_id,
        summary=summary
    )

    return {
        "answer": result["answer"],
        "conversation_id": result["conversation_id"],
        "summary": summary
    }
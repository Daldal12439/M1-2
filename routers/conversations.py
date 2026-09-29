from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/conversations",
    tags=["conversations"]
)


class Message(BaseModel):
    role: str = Field(
        min_length=1,
        max_length=20
    )

    content: str = Field(
        min_length=1,
        max_length=10000
    )


class ConversationCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200
    )

    messages: list[Message] = Field(
        default_factory=list
    )


class ConversationResponse(BaseModel):
    id: str
    title: str
    messages: list[Message]


class ConversationDeleteResponse(BaseModel):
    message: str
    id: str


@router.post(
    "",
    response_model=ConversationResponse
)
def create_conversation(
    conversation: ConversationCreate
):
    from main import db

    doc_ref = (
        db.collection("conversations")
        .document()
    )

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


@router.get(
    "",
    response_model=list[ConversationResponse]
)
def get_conversations():
    from main import db

    docs = (
        db.collection("conversations")
        .stream()
    )

    result = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        result.append(data)

    return result


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation(
    conversation_id: str
):
    from main import db

    doc_ref = (
        db.collection("conversations")
        .document(conversation_id)
    )

    doc = doc_ref.get()

    if not doc.exists:
        return {
            "id": conversation_id,
            "title": "대화를 찾을 수 없습니다.",
            "messages": []
        }

    data = doc.to_dict()
    data["id"] = doc.id

    return data


@router.delete(
    "/{conversation_id}",
    response_model=ConversationDeleteResponse
)
def delete_conversation(
    conversation_id: str
):
    from main import db

    doc_ref = (
        db.collection("conversations")
        .document(conversation_id)
    )

    if not doc_ref.get().exists:
        return {
            "message": "대화를 찾을 수 없습니다.",
            "id": conversation_id
        }

    doc_ref.delete()

    return {
        "message": "대화가 삭제되었습니다.",
        "id": conversation_id
    }
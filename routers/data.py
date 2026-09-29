from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/data",
    tags=["data"]
)


class DataCreate(BaseModel):
    date: str = Field(
        min_length=1,
        max_length=20
    )

    value: float = Field(
        ge=-1000000,
        le=1000000
    )

    memo: str = Field(
        default="",
        max_length=500
    )


class DataResponse(BaseModel):
    id: str
    date: str
    value: float
    memo: str


class DataDeleteResponse(BaseModel):
    message: str
    id: str


@router.get(
    "",
    response_model=list[DataResponse]
)
def get_data():
    from main import db

    docs = db.collection("data").stream()

    result = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        result.append(data)

    return result


@router.post(
    "",
    response_model=DataResponse
)
def create_data(data: DataCreate):
    from main import db

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


@router.put(
    "/{data_id}",
    response_model=DataResponse
)
def update_data(
    data_id: str,
    data: DataCreate
):
    from main import db

    doc_ref = db.collection("data").document(data_id)

    if not doc_ref.get().exists:
        return {
            "id": data_id,
            "date": data.date,
            "value": data.value,
            "memo": data.memo
        }

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


@router.delete(
    "/{data_id}",
    response_model=DataDeleteResponse
)
def delete_data(data_id: str):
    from main import db

    doc_ref = db.collection("data").document(data_id)

    if not doc_ref.get().exists:
        return {
            "message": "데이터를 찾을 수 없습니다.",
            "id": data_id
        }

    doc_ref.delete()

    return {
        "message": "데이터가 삭제되었습니다.",
        "id": data_id
    }
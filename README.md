# AI Assistant

개인 데이터를 저장하고 관리하며, 저장된 데이터를 요약하여 AI와 대화할 수 있는 웹 기반 개인 비서 프로젝트이다.

## 1. 프로젝트 개요

이 프로젝트는 사용자가 날짜별 데이터를 등록하고 수정·삭제할 수 있으며, 저장된 데이터를 바탕으로 통계 요약을 제공하고 AI에게 자연어로 질문할 수 있도록 구현하였다.

주요 기능은 다음과 같다.

* 데이터 추가
* 데이터 조회
* 데이터 수정
* 데이터 삭제
* 데이터 통계 요약
* 저장된 데이터 요약 정보를 AI 프롬프트에 주입
* AI와의 대화
* 대화 자동 저장
* 저장된 대화 목록 조회
* 기존 대화 불러오기
* 새 대화 시작
* 데스크톱 3단 레이아웃 UI
* 모바일 반응형 UI

---

## 2. 기술 스택

### Frontend

* HTML
* CSS
* JavaScript
* Fetch API

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### Database

* Firebase Firestore

### AI

* OpenAI API
* `gpt-4o-mini`

### 개발 환경

* Windows
* Python Virtual Environment (`.venv`)

---

## 3. 프로젝트 구조

```text
ai-assistant/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── routers/
│   ├── data.py
│   └── conversations.py
│
├── services/
│   ├── ai_service.py
│   └── summary_service.py
│
├── main.py
├── import_data.py
├── check_data.py
├── OBS_ASOS_DD_20260922162003.csv
├── .env
├── .gitignore
└── README.md
```

### 파일별 역할

| 파일                               | 역할                                                         |
| -------------------------------- | ---------------------------------------------------------- |
| `main.py`                        | FastAPI 앱 초기화, CORS/Firebase/OpenAI 연결, 라우터 등록 및 핵심 API 연결 |
| `routers/data.py`                | 데이터 CRUD API                                               |
| `routers/conversations.py`       | 대화 CRUD API                                                |
| `services/summary_service.py`    | Firestore 데이터를 읽어 통계 및 추세 요약                               |
| `services/ai_service.py`         | 기존 대화 조회, system prompt 구성, OpenAI API 호출, 대화 저장           |
| `import_data.py`                 | CSV 데이터를 Firestore에 등록                                     |
| `check_data.py`                  | 데이터 확인 및 테스트용 스크립트                                         |
| `frontend/index.html`            | 웹 페이지 구조                                                   |
| `frontend/script.js`             | API 호출, 대화 상태 및 화면 동작                                      |
| `frontend/style.css`             | 화면 레이아웃, 스타일 및 반응형 UI                                      |
| `OBS_ASOS_DD_20260922162003.csv` | 분석 및 테스트에 사용한 원본 데이터                                       |
| `.env`                           | API 키 및 Firebase 관련 환경변수                                   |
| `.gitignore`                     | 민감정보 및 가상환경 파일 제외                                          |

---

## 4. 실행 방법

### 4.1 가상환경 활성화

Windows PowerShell에서 프로젝트 폴더로 이동한다.

```powershell
cd C:\Users\Codyssey\Desktop\ai-assistant
```

가상환경을 활성화한다.

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4.2 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 필요한 환경변수를 설정한다.

```env
OPENAI_API_KEY=your_openai_api_key
FIREBASE_SERVICE_ACCOUNT_JSON=your_firebase_service_account_json
```

`OPENAI_API_KEY`는 OpenAI API 인증에 사용한다.

`FIREBASE_SERVICE_ACCOUNT_JSON`은 Firebase Admin SDK가 Firestore에 접근하기 위한 서비스 계정 JSON 파일의 경로이다.

실제 API 키와 Firebase 인증정보는 GitHub에 업로드하지 않는다.

### 4.3 백엔드 실행

```powershell
uvicorn main:app --reload
```

백엔드는 기본적으로 다음 주소에서 실행된다.

```text
http://127.0.0.1:8000
```

FastAPI Swagger 문서는 다음 주소에서 확인할 수 있다.

```text
http://127.0.0.1:8000/docs
```

### 4.4 프론트엔드 실행

백엔드와 별도의 PowerShell 창에서 다음 명령을 실행한다.

```powershell
cd C:\Users\Codyssey\Desktop\ai-assistant\frontend
python -m http.server 5500
```

브라우저에서 다음 주소로 접속한다.

```text
http://localhost:5500/
```

프론트엔드와 백엔드를 각각 실행해야 하므로 두 개의 터미널을 사용하는 구조이다.

---

## 5. 주요 API

### 데이터

| Method | Endpoint              | 설명             |
| ------ | --------------------- | -------------- |
| GET    | `/api/data`           | 데이터 목록 조회      |
| POST   | `/api/data`           | 데이터 추가         |
| PUT    | `/api/data/{data_id}` | 데이터 수정         |
| DELETE | `/api/data/{data_id}` | 데이터 삭제         |
| GET    | `/api/data/summary`   | 데이터 통계 및 추세 요약 |

### 대화

| Method | Endpoint                               | 설명        |
| ------ | -------------------------------------- | --------- |
| GET    | `/api/conversations`                   | 대화 목록 조회  |
| POST   | `/api/conversations`                   | 새로운 대화 생성 |
| GET    | `/api/conversations/{conversation_id}` | 특정 대화 조회  |
| DELETE | `/api/conversations/{conversation_id}` | 대화 삭제     |

### AI

| Method | Endpoint    | 설명                     |
| ------ | ----------- | ---------------------- |
| POST   | `/api/chat` | 사용자 질문을 AI에 전달하고 응답 저장 |

---

## 6. Firestore 설계

프로젝트에서는 역할에 따라 두 개의 컬렉션을 사용한다.

### `data`

날짜별 측정 데이터를 저장한다.

예시:

```text
data
└── document
    ├── date: "2024-01-01"
    ├── value: 3.2
    └── memo: "측정 데이터"
```

| 필드      | 타입     | 설명     |
| ------- | ------ | ------ |
| `date`  | string | 데이터 날짜 |
| `value` | number | 측정값    |
| `memo`  | string | 추가 메모  |

현재 데이터 조회 및 요약은 Firestore의 `data` 컬렉션 전체를 읽은 후 애플리케이션에서 처리하는 방식으로 구현하였다.

현재 프로젝트에서 사용한 데이터 규모에서는 이 방식으로 기능을 구현하였다.

데이터 규모가 증가할 경우 날짜 조건을 활용한 Firestore 쿼리, 인덱스 및 페이징을 적용하여 읽기 비용과 응답 시간을 줄일 수 있다.

### `conversations`

AI 대화 내용을 저장한다.

예시:

```text
conversations
└── document
    ├── title: "데이터 기간 질문"
    └── messages:
        ├── role: "user"
        │   content: "저장된 데이터는 어떤 기간의 데이터야?"
        └── role: "assistant"
            content: "2023-01-01 ~ 2024-12-31입니다."
```

| 필드                   | 타입     | 설명                    |
| -------------------- | ------ | --------------------- |
| `title`              | string | 대화 제목                 |
| `messages`           | array  | 대화 메시지 목록             |
| `messages[].role`    | string | `user` 또는 `assistant` |
| `messages[].content` | string | 메시지 내용                |

현재는 개인 프로젝트 규모를 고려하여 별도의 복잡한 인덱스나 사용자별 분리 없이 구현하였다.

실제 서비스로 확장할 경우 사용자 ID를 기준으로 데이터를 분리하고 접근 권한을 관리할 필요가 있다.

---

## 7. 데이터 요약

`GET /api/data/summary`는 `services/summary_service.py`의 `get_summary()` 함수를 사용하여 저장된 데이터를 요약한다.

예시 응답:

```json
{
  "period": "2023-01-01 ~ 2024-12-31",
  "count": 731,
  "metrics": {
    "average": 14.52,
    "max": 30.7,
    "min": -11.4
  },
  "trend": "상승"
}
```

### 제공 정보

* `period`: 데이터의 시작일과 종료일
* `count`: 전체 데이터 개수
* `average`: 평균값
* `max`: 최고값
* `min`: 최저값
* `trend`: 최근 데이터의 변화 방향

현재 프로젝트에서 사용한 데이터는 2023-01-01부터 2024-12-31까지 총 731개이다.

### 추세 계산

데이터가 14개 이상 존재하는 경우 날짜순으로 정렬한 뒤 다음 두 구간의 평균값을 비교한다.

* 최근 7개 데이터
* 그 이전 7개 데이터

두 구간의 평균 차이가 다음 조건에 따라 추세로 표시된다.

```text
차이 > 0.5       → 상승
차이 < -0.5      → 하락
그 외            → 유지
```

14개 미만인 경우 `데이터 부족`으로 표시한다.

데이터가 존재하지 않는 경우 `데이터 없음`으로 표시한다.

현재 요약 기능은 별도의 서비스 함수로 분리되어 `/api/data/summary`와 AI 채팅에서 공통으로 사용한다.

향후에는 기간을 파라미터로 받아 특정 기간만 요약할 수 있도록 확장할 수 있다.

예:

```text
/api/data/summary?start_date=2024-01-01&end_date=2024-12-31
```

---

## 8. AI 컨텍스트 주입

AI 채팅 요청이 들어오면 `summary_service.py`에서 현재 저장된 데이터의 요약 정보를 생성한다.

생성된 요약은 `ai_service.py`에서 OpenAI에 전달하는 system prompt에 포함한다.

구조는 다음과 같다.

```text
사용자 질문
    ↓
/api/chat
    ↓
데이터 요약 생성
    ↓
system prompt에 요약 정보 주입
    ↓
OpenAI API
    ↓
AI 응답
    ↓
대화 저장
```

System prompt에는 현재 저장된 데이터의 기간, 개수, 평균, 최고값, 최저값 및 추세가 포함된다.

이를 통해 AI가 일반적인 답변만 생성하는 것이 아니라 현재 저장된 데이터의 요약 정보를 참고하여 답변하도록 구성하였다.

### 장점

* AI가 원본 데이터 전체를 매번 직접 처리하지 않아도 된다.
* 요약된 핵심 정보만 전달하므로 원본 데이터 전체를 프롬프트에 넣는 것보다 입력 데이터량을 줄일 수 있다.
* 데이터 요약 로직과 AI 채팅 로직을 분리하여 요약 기능을 다른 API나 화면에서도 재사용할 수 있다.
* AI가 데이터에 없는 내용을 추측하지 않도록 system prompt에서 제한한다.

### 고려사항

현재 구조에서는 AI 질문이 들어올 때마다 Firestore 데이터를 읽어 요약을 다시 계산한다.

따라서 데이터 규모나 요청 횟수가 증가하면 다음 요소가 증가할 수 있다.

* Firestore 읽기 작업
* 서버의 데이터 처리량
* OpenAI API 요청 횟수
* AI 입력 토큰 사용량 및 비용

또한 현재 대화의 이전 메시지도 AI 요청에 함께 전달하므로 대화가 길어질수록 입력 토큰이 증가할 수 있다.

향후에는 다음과 같은 방법을 고려할 수 있다.

* 데이터 요약 결과 캐싱
* 데이터 변경 시에만 요약 갱신
* 긴 대화의 이전 메시지 요약
* 대화 메시지 길이 제한
* 필요한 데이터만 조회하는 기간 조건 쿼리

---

## 9. 대화 저장 방식

AI 응답이 성공적으로 생성된 후 사용자 메시지와 AI 응답을 하나의 대화 문서에 저장한다.

메시지는 다음과 같은 형태를 사용한다.

```json
{
  "role": "user",
  "content": "질문 내용"
}
```

또는

```json
{
  "role": "assistant",
  "content": "AI 답변"
}
```

### 저장 시점

AI 응답 생성이 성공한 후 대화를 저장한다.

이 방식을 사용하는 이유는 실패한 AI 요청을 정상적인 대화 기록으로 저장하지 않기 위해서이다.

### 새 대화

`conversation_id`가 없는 요청은 새로운 Firestore 문서를 생성한다.

첫 번째 사용자 질문의 앞부분을 대화 제목으로 사용한다.

```text
title = 사용자 질문의 앞 30자
```

### 기존 대화

`conversation_id`가 있는 경우 해당 대화의 기존 메시지를 Firestore에서 불러온 후 새로운 사용자 질문과 AI 응답을 뒤에 추가한다.

### 대화 불러오기

왼쪽 대화 목록에서 대화를 선택하면 `/api/conversations/{conversation_id}`를 호출하여 저장된 메시지를 조회하고 화면에 표시한다.

---

## 10. Frontend 상태 관리

현재 프론트엔드는 별도의 상태 관리 라이브러리를 사용하지 않고 JavaScript 변수와 DOM을 이용하여 상태를 관리한다.

주요 상태는 다음과 같다.

```javascript
let currentConversationId = null;

let editingDataId = null;
```

* `currentConversationId`: 현재 선택된 대화 ID
* `editingDataId`: 현재 수정 중인 데이터 ID

상태 흐름은 다음과 같다.

```text
사용자 입력
    ↓
JavaScript 이벤트
    ↓
FastAPI API 호출
    ↓
응답 수신
    ↓
상태 변수 갱신
    ↓
DOM 갱신
```

현재 프로젝트 규모에서는 별도의 상태 관리 라이브러리 없이 이 방식으로 구현하였다.

프로젝트 규모가 커질 경우 컴포넌트 기반 프레임워크나 중앙 상태 관리 방식을 도입할 수 있다.

---

## 11. 라우터 및 서비스 책임 분리

현재 구현에서는 기능별 책임을 `routers`와 `services`로 분리하였다.

구조는 다음과 같다.

```text
main.py
│
├── FastAPI 앱 초기화
├── CORS 설정
├── Firebase 연결
├── OpenAI 연결
└── Router 등록
       │
       ├── routers/data.py
       │      └── 데이터 CRUD
       │
       ├── routers/conversations.py
       │      └── 대화 CRUD
       │
       └── services/
              ├── summary_service.py
              │      └── 데이터 요약
              │
              └── ai_service.py
                     └── AI 호출 및 대화 저장
```

### 책임

* `main.py`: 애플리케이션 초기화 및 의존성 연결
* `routers`: HTTP 요청과 응답 및 API 엔드포인트 담당
* `services`: 데이터 처리와 주요 비즈니스 로직 담당

이 구조를 사용하면 특정 기능을 수정할 때 다른 기능의 코드와 분리하여 관리할 수 있다.

예를 들어 데이터 요약 방식은 `summary_service.py`에서 수정할 수 있고, AI 호출 방식은 `ai_service.py`에서 수정할 수 있다.

---

## 12. 입력 검증

FastAPI에서는 Pydantic 모델을 사용하여 API 요청의 타입과 기본적인 입력 범위를 검증한다.

예를 들어 데이터 추가 및 수정 요청은 다음과 같은 제약을 가진다.

```python
class DataCreate(BaseModel):
    date: str = Field(min_length=1, max_length=20)
    value: float = Field(ge=-1000000, le=1000000)
    memo: str = Field(default="", max_length=500)
```

AI 채팅 요청은 다음과 같이 질문 길이를 제한한다.

```python
class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000
    )

    conversation_id: str | None = None
```

대화 메시지도 역할과 내용의 길이를 제한한다.

잘못된 요청은 FastAPI/Pydantic의 validation을 통해 `422 Unprocessable Entity` 응답으로 처리된다.

### 현재 적용된 검증

* 데이터 날짜: 1~20자
* 데이터 값: -1,000,000~1,000,000
* 데이터 메모: 최대 500자
* AI 질문: 1~5,000자
* 대화 제목: 1~200자
* 대화 메시지 내용: 1~10,000자

### Frontend 출력 보안

사용자 메시지와 AI 응답을 화면에 표시할 때 HTML이 직접 DOM으로 해석되지 않도록 `textContent` 기반으로 출력한다.

따라서 사용자 입력에 포함된 HTML 태그가 화면의 HTML 구조로 실행되는 것을 방지한다.

### 추가 고려사항

현재는 기본적인 입력 검증과 화면 출력 처리를 적용하였다.

실제 서비스로 확장할 경우 다음과 같은 보안 기능을 추가할 수 있다.

* 날짜 형식 검증
* 인증 및 사용자별 접근 권한
* API 요청 빈도 제한
* 더욱 엄격한 입력 검증
* 서버 측 로깅 및 오류 모니터링
* Firestore Security Rules 적용

---

## 13. 환경변수 및 보안

API 키와 Firebase 인증정보는 소스 코드에 직접 작성하지 않고 환경변수로 관리한다.

`.gitignore`에는 다음 항목이 포함되어 있다.

```text
.venv/
__pycache__/
.env
firebase-service-account.json
```

따라서 다음 파일과 디렉터리는 GitHub에 업로드하지 않는다.

* `.env`
* `firebase-service-account.json`
* `.venv/`

### 배포 시

Render, Railway 등의 서버 환경을 사용할 경우 플랫폼의 Environment Variables 기능을 이용하여 API 키와 Firebase 인증정보를 설정할 수 있다.

프론트엔드에서 사용하는 백엔드 URL은 현재 로컬 환경에서 다음과 같다.

```text
http://127.0.0.1:8000
```

실제 배포 시에는 배포된 백엔드의 HTTPS URL로 변경해야 한다.

또한 Firebase 서비스 계정 인증정보도 배포 환경의 안전한 환경변수 또는 Secret 관리 기능을 이용하여 제공해야 한다.

---

## 14. CORS

현재 로컬 개발 환경을 위해 다음 두 개의 프론트엔드 주소를 허용한다.

```text
http://127.0.0.1:5500
http://localhost:5500
```

FastAPI에서는 다음과 같이 설정되어 있다.

```python
allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
```

배포 시에는 실제 프론트엔드 도메인만 허용하도록 `allow_origins`를 변경해야 한다.

예:

```python
allow_origins=[
    "https://배포된-프론트엔드-주소"
]
```

운영 환경에서는 불필요하게 모든 Origin을 허용하지 않는 것을 원칙으로 한다.

---

## 15. 반응형 UI

현재 화면은 데스크톱에서 다음과 같은 3단 구조로 표시된다.

```text
┌──────────┬──────────────────────┬──────────┐
│ 대화목록 │       AI 채팅        │ 데이터   │
│          │                      │ 요약/관리│
└──────────┴──────────────────────┴──────────┘
```

CSS 미디어 쿼리를 사용하여 화면 크기에 따라 레이아웃을 변경한다.

### Desktop

```text
대화목록 | AI 채팅 | 데이터 관리
```

### Tablet

화면 크기에 맞춰 각 영역의 크기를 조정한다.

### Mobile

모바일에서는 AI 채팅을 중심으로 표시하고 대화 목록과 데이터 관리 패널을 별도로 열 수 있도록 구성하였다.

```text
┌─────────────────────┐
│ ☰ 대화 목록  📊 데이터 │
├─────────────────────┤
│                     │
│       AI 채팅        │
│                     │
├─────────────────────┤
│ 입력창       전송     │
└─────────────────────┘
```

모바일에서 대화 목록과 데이터 관리 영역은 슬라이드 패널 형태로 표시된다.

---

## 16. 콜드스타트 및 운영 고려사항

현재 프로젝트는 로컬 개발 환경에서 실행하는 것을 기준으로 한다.

클라우드 서버에 배포할 경우 무료 또는 저사양 서버에서는 일정 시간 요청이 없을 때 서버가 sleep 상태가 될 수 있으며, 첫 요청에 추가 응답 시간이 발생할 수 있다.

이를 일반적으로 콜드스타트라고 한다.

운영 환경에서는 다음 방법을 고려할 수 있다.

* 서버 상태 확인용 health check endpoint 추가
* 외부 모니터링 서비스의 주기적 요청
* 상시 실행 서버 사용
* 프론트엔드에서 초기 로딩 상태 표시

현재 프론트엔드는 API 요청 중 로딩 메시지와 버튼 상태 변경을 사용하여 사용자가 요청 처리 상태를 확인할 수 있도록 구성하였다.

향후 배포 시 서버 플랫폼의 sleep 정책과 초기 요청 지연 여부를 확인할 필요가 있다.

---

## 17. API 테스트

FastAPI Swagger UI에서 API를 직접 테스트할 수 있다.

```text
http://127.0.0.1:8000/docs
```

예를 들어 데이터 요약 API를 실행하면 다음과 같은 결과를 확인할 수 있다.

```json
{
  "period": "2023-01-01 ~ 2024-12-31",
  "count": 731,
  "metrics": {
    "average": 14.52,
    "max": 30.7,
    "min": -11.4
  },
  "trend": "상승"
}
```

AI 채팅에서는 다음과 같은 질문을 통해 저장 데이터 활용 여부를 확인할 수 있다.

```text
저장된 데이터의 평균값과 최고값, 최저값을 알려줘.
```

실제 테스트에서는 저장된 데이터의 요약값을 바탕으로 다음과 같은 답변이 정상적으로 생성되는 것을 확인하였다.

```text
저장된 데이터의 평균값은 14.52, 최고값은 30.7, 최저값은 -11.4입니다.
```

Swagger UI에서는 Pydantic의 요청 및 응답 모델도 확인할 수 있다.

---

## 18. 현재 테스트 결과

현재 로컬 환경에서 다음 기능을 확인하였다.

* 데이터 추가 정상 작동
* 데이터 조회 정상 작동
* 데이터 수정 정상 작동
* 데이터 삭제 정상 작동
* 데이터 요약 정상 작동
* AI의 저장 데이터 활용 정상 작동
* 대화 저장 정상 작동
* 대화 목록 표시 정상 작동
* 기존 대화 불러오기 정상 작동
* 새 대화 시작 정상 작동
* 데이터 관리 영역 자체 스크롤 정상 작동
* 모바일 반응형 UI 정상 작동
* FastAPI Swagger 문서 정상 작동
* Router/Service 분리 후 API 정상 작동

---

## 19. 배포

현재 버전은 로컬 개발 환경을 기준으로 한다.

### Frontend

```text
http://localhost:5500/
```

### Backend

```text
http://127.0.0.1:8000
```

### Swagger

```text
http://127.0.0.1:8000/docs
```

현재는 실제 외부 서비스에 배포된 URL이 없는 상태이다.

실제 서비스 배포 시에는 다음 작업이 필요하다.

1. FastAPI 백엔드 배포
2. OpenAI API 키 환경변수 등록
3. Firebase 인증정보 환경변수 등록
4. 프론트엔드의 `API_BASE_URL`을 배포된 백엔드 HTTPS 주소로 변경
5. CORS에 배포된 프론트엔드 도메인 등록
6. HTTPS 적용
7. 배포된 서비스의 정상 동작 확인
8. 필요할 경우 health check 및 모니터링 구성

---

## 20. 향후 개선 사항

* 실제 서비스 배포
* 사용자 인증 및 권한 관리
* 사용자별 Firestore 데이터 분리
* 데이터 기간 필터 추가
* Firestore 기간 조건 쿼리 및 인덱스 최적화
* 대화 목록 페이징
* 긴 대화의 메시지 요약 및 토큰 절감
* 데이터 요약 캐싱
* API 오류 처리 및 로깅 개선
* health check endpoint 추가
* 운영 환경 모니터링
* 날짜 형식 검증 강화
* API 요청 빈도 제한
* 테스트 코드 추가

---

## 21. GitHub

프로젝트 저장소:

https://github.com/Daldal12439/M1-2

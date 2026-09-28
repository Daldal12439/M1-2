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
* 웹 기반 3단 레이아웃 UI

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

* Google Gemini API

### 개발 환경

* Windows
* Python Virtual Environment (`.venv`)

---

## 3. 프로젝트 구조

```text
ai-assistant/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── main.py
├── import_data.py
├── check_data.py
├── OBS_ASOS_DD_20260922162003.csv
├── .env
├── .gitignore
└── README.md
```

### 파일별 역할

| 파일                               | 역할                                                    |
| -------------------------------- | ----------------------------------------------------- |
| `main.py`                        | FastAPI 서버, Firestore 연동, 데이터 CRUD, 요약, 대화, AI 채팅 API |
| `import_data.py`                 | CSV 데이터를 Firestore에 등록                                |
| `check_data.py`                  | 데이터 확인 및 테스트용 스크립트                                    |
| `frontend/index.html`            | 웹 페이지 구조                                              |
| `frontend/script.js`             | API 호출 및 화면 동작                                        |
| `frontend/style.css`             | 화면 레이아웃 및 스타일                                         |
| `OBS_ASOS_DD_20260922162003.csv` | 분석 및 테스트에 사용한 원본 데이터                                  |
| `.env`                           | API 키 및 Firebase 관련 환경변수                              |
| `.gitignore`                     | 민감정보 및 가상환경 파일 제외                                     |

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

프로젝트 루트에 `.env` 파일을 생성하고 필요한 API 및 Firebase 환경변수를 설정한다.

예시는 다음과 같다.

```env
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_SERVICE_ACCOUNT_JSON=your_firebase_service_account_json
```

실제 API 키와 인증정보는 GitHub에 업로드하지 않는다.

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

별도의 PowerShell 창에서 다음 명령을 실행한다.

```powershell
cd C:\Users\Codyssey\Desktop\ai-assistant\frontend
python -m http.server 5500
```

브라우저에서 다음 주소로 접속한다.

```text
http://localhost:5500/
```

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

현재 데이터 조회 및 요약은 전체 데이터를 읽은 후 날짜를 기준으로 정렬하는 방식으로 구현하였다.

향후 데이터 규모가 커질 경우 날짜 필드에 대한 Firestore 인덱스와 기간 조건 쿼리를 적용하여 읽기 비용과 응답 시간을 줄일 수 있다.

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

현재 개인 프로젝트 규모를 고려하여 별도의 복잡한 인덱스 없이 구현하였다.

---

## 7. 데이터 요약

`GET /api/data/summary`에서 저장된 데이터를 기준으로 다음 정보를 계산한다.

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

현재 추세는 데이터가 충분할 경우 최근 데이터를 기준으로 이전 구간과 비교하여 상승·하락 여부를 판단한다.

코드의 요약 기준을 변경하려면 `main.py`의 `/api/data/summary` 로직을 수정한다.

향후에는 다음과 같이 기간을 파라미터로 받을 수 있도록 확장할 수 있다.

```text
/api/data/summary?start_date=2024-01-01&end_date=2024-12-31
```

---

## 8. AI 컨텍스트 주입

AI 채팅 요청이 들어오면 현재 저장된 데이터의 요약 정보를 먼저 생성한다.

생성된 요약은 Gemini에게 전달하는 system prompt에 포함한다.

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
Gemini API
    ↓
AI 응답
    ↓
대화 저장
```

이를 통해 AI가 단순히 일반적인 답변을 생성하는 것이 아니라 현재 저장된 데이터의 평균·최고·최저·기간 등의 정보를 참고하여 답변하도록 구성하였다.

### 장점

* AI가 현재 저장된 데이터의 전체 내용을 매번 직접 처리하지 않아도 된다.
* 요약된 핵심 정보만 전달하므로 프롬프트의 불필요한 데이터량을 줄일 수 있다.
* 데이터 요약 로직과 AI 채팅 로직이 분리되어 다른 화면이나 기능에서도 요약 API를 재사용할 수 있다.

### 고려사항

요약 정보 자체는 원본 데이터 전체보다 크기가 작지만, 모든 질문마다 요약을 생성하고 AI 프롬프트에 포함하기 때문에 요청 횟수가 증가하면 API 사용량과 비용에 영향을 줄 수 있다.

향후에는 캐싱이나 요약 갱신 주기를 적용하여 불필요한 반복 계산을 줄일 수 있다.

---

## 9. 대화 저장 방식

AI 응답이 생성된 후 사용자 메시지와 AI 응답을 하나의 대화에 저장한다.

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

이 방식을 선택한 이유는 실패한 AI 요청을 정상적인 대화 기록으로 저장하지 않기 위해서이다.

### 불러오기

왼쪽 대화 목록에서 대화를 선택하면 저장된 메시지를 조회하여 화면에 다시 표시한다.

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

현재 프로젝트 규모에서는 이 방식으로 충분하다고 판단하였다.

프로젝트 규모가 커질 경우 중앙 상태 관리 또는 컴포넌트 기반 프레임워크를 도입할 수 있다.

---

## 11. 라우터 및 서비스 책임 분리

현재 구현에서는 빠른 프로토타이핑과 프로젝트 규모를 고려하여 API와 주요 로직을 `main.py`에 통합하였다.

현재 구조:

```text
main.py
├── FastAPI 설정
├── CORS 설정
├── Pydantic 요청 모델
├── 데이터 CRUD
├── 데이터 요약
├── 대화 CRUD
└── AI 채팅
```

향후 유지보수성과 확장성을 높이기 위해 다음과 같이 분리할 수 있다.

```text
app/
├── main.py
├── routers/
│   ├── data.py
│   ├── conversations.py
│   └── chat.py
├── services/
│   ├── data_service.py
│   ├── conversation_service.py
│   └── ai_service.py
└── schemas/
    └── models.py
```

### 책임

* `routers`: HTTP 요청과 응답 담당
* `services`: 데이터 처리 및 비즈니스 로직 담당
* `schemas`: 요청/응답 데이터 구조 담당
* `main.py`: 애플리케이션 초기화 및 라우터 등록

현재는 프로젝트 규모가 작아 단일 파일 구조를 사용했으며, 기능이 증가하면 위 구조로 분리할 수 있다.

---

## 12. 입력 검증

FastAPI에서는 Pydantic 모델을 사용하여 요청 데이터의 기본적인 타입 검증을 수행한다.

예:

```python
class DataCreate(BaseModel):
    date: str
    value: float
    memo: str
```

```python
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
```

향후 운영 환경에서는 다음과 같은 검증을 추가할 수 있다.

* 날짜 형식 검증
* 숫자 범위 제한
* 메모 최대 길이 제한
* 질문 최대 길이 제한
* 허용되지 않는 입력 패턴 검증
* 사용자 입력을 HTML로 직접 렌더링하지 않도록 처리

현재 프론트엔드 메시지는 `textContent` 방식으로 화면에 출력하여 HTML 태그가 DOM으로 해석되지 않도록 구현하였다.

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

따라서 다음 파일은 GitHub에 업로드하지 않는다.

* `.env`
* `firebase-service-account.json`
* `.venv/`

### 배포 시

Render, Railway 등의 서버 환경에서는 플랫폼의 Environment Variables 기능을 이용하여 API 키와 Firebase 인증정보를 설정한다.

프론트엔드에서 사용하는 백엔드 URL 역시 로컬 환경에서는 다음 주소를 사용한다.

```text
http://127.0.0.1:8000
```

실제 배포 시에는 배포된 백엔드 HTTPS URL로 변경해야 한다.

---

## 14. CORS

현재 로컬 개발 환경을 위해 다음과 같은 프론트엔드 주소를 허용한다.

```text
http://127.0.0.1:5500
http://localhost:5500
```

배포 시에는 실제 프론트엔드 도메인만 허용하도록 `allow_origins`를 변경한다.

예:

```python
allow_origins=[
    "https://배포된-프론트엔드-주소"
]
```

운영 환경에서는 불필요하게 모든 Origin을 허용하지 않는 것을 원칙으로 한다.

---

## 15. 반응형 UI

현재 기본 화면은 다음과 같은 3단 구조이다.

```text
┌──────────┬──────────────────────┬──────────┐
│ 대화목록 │      AI 채팅         │ 데이터   │
│          │                      │ 요약/관리│
└──────────┴──────────────────────┴──────────┘
```

현재 데스크톱 화면을 기준으로 구현되어 있다.

향후 모바일 및 작은 화면을 지원하기 위해 CSS 미디어쿼리를 추가하여 다음과 같이 변경할 수 있다.

```text
Desktop
대화목록 | AI 채팅 | 데이터 관리

Tablet
대화목록
AI 채팅
데이터 관리

Mobile
AI 채팅
대화목록
데이터 관리
```

특히 작은 화면에서는 입력창과 전송 버튼이 항상 보이도록 레이아웃을 재배치할 예정이다.

---

## 16. 콜드스타트 및 운영 고려사항

현재 프로젝트는 로컬 개발 환경에서 실행하는 것을 기준으로 한다.

클라우드 서버에 배포할 경우 무료 또는 저사양 서버에서는 일정 시간 요청이 없을 때 서버가 sleep 상태가 될 수 있으며, 첫 요청에 추가 응답 시간이 발생할 수 있다.

이를 콜드스타트라고 한다.

운영 환경에서는 다음 방법을 고려할 수 있다.

* 서버 상태 확인용 health check endpoint 추가
* 외부 모니터링 서비스의 주기적 요청
* 유료 또는 상시 실행 서버 사용
* 프론트엔드에서 초기 로딩 상태 표시

현재 프론트엔드에서는 API 요청 중 로딩 메시지와 버튼 상태 변경을 사용하여 사용자가 요청 처리 상태를 확인할 수 있도록 구성하였다.

---

## 17. API 테스트 예시

Swagger UI에서 API를 직접 테스트할 수 있다.

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

응답 예시:

```text
저장된 데이터의 평균값은 14.52, 최고값은 30.7, 최저값은 -11.4입니다.
```

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

실제 서비스 배포 시에는 다음 작업이 필요하다.

1. FastAPI 백엔드 배포
2. Gemini API 및 Firebase 환경변수 등록
3. 프론트엔드의 `API_BASE_URL`을 배포된 백엔드 주소로 변경
4. CORS에 배포된 프론트엔드 도메인 등록
5. HTTPS 적용
6. 배포된 서비스의 정상 동작 확인

---

## 20. 향후 개선 사항

* 프론트엔드 반응형 지원
* 라우터와 서비스 계층 분리
* Pydantic 응답 모델 추가
* 날짜 및 숫자 범위 검증 강화
* 입력 길이 및 패턴 검증 강화
* 데이터 기간 필터 추가
* Firestore 쿼리 및 인덱스 최적화
* 대화 목록 페이징
* 사용자 인증 및 권한 관리
* API 오류 처리 및 로깅 개선
* 배포 환경 구성
* health check 및 운영 모니터링 추가

---

## 21. GitHub

프로젝트 저장소:

https://github.com/Daldal12439/M1-2

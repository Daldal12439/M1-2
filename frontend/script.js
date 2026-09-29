const API_BASE_URL = "https://ai-assistant-n8nl.onrender.com";

let currentConversationId = null;
let editingDataId = null;


// 요소 가져오기
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat-button");
const chatMessages = document.getElementById("chat-messages");
const conversationList = document.getElementById("conversation-list");
const summaryContent = document.getElementById("summary-content");

const dataDate = document.getElementById("data-date");
const dataValue = document.getElementById("data-value");
const dataMemo = document.getElementById("data-memo");
const addDataButton = document.getElementById("add-data-button");
const dataList = document.getElementById("data-list");

const mobileConversationButton =
    document.getElementById("mobile-conversation-button");

const mobileDataButton =
    document.getElementById("mobile-data-button");

const sidebar =
    document.querySelector(".sidebar");

const summaryPanel =
    document.querySelector(".summary-panel");


// 페이지 시작
document.addEventListener("DOMContentLoaded", () => {
    loadConversations();
    loadSummary();
    loadData();
});


// ==============================
// 모바일 메뉴
// ==============================

mobileConversationButton.addEventListener(
    "click",
    () => {
        sidebar.classList.toggle("mobile-open");

        summaryPanel.classList.remove("mobile-open");
    }
);


mobileDataButton.addEventListener(
    "click",
    () => {
        summaryPanel.classList.toggle("mobile-open");

        sidebar.classList.remove("mobile-open");
    }
);


// 모바일 패널 닫기
function closeMobilePanels() {
    sidebar.classList.remove("mobile-open");
    summaryPanel.classList.remove("mobile-open");
}


// ==============================
// 데이터 목록 불러오기
// ==============================

async function loadData() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/data`
        );

        if (!response.ok) {
            throw new Error(
                "데이터 목록을 불러오지 못했습니다."
            );
        }

        const data = await response.json();

        dataList.innerHTML = "";

        if (data.length === 0) {
            dataList.innerHTML =
                '<p class="empty-message">데이터가 없습니다.</p>';
            return;
        }

        const recentData = data
            .sort(
                (a, b) =>
                    b.date.localeCompare(a.date)
            )
            .slice(0, 10);

        recentData.forEach(item => {
            const itemElement =
                document.createElement("div");

            itemElement.className = "data-item";

            itemElement.innerHTML = `
                <div>
                    <strong>${item.date}</strong>
                    <span>${item.value}</span>
                    <small>${item.memo || ""}</small>
                </div>

                <div class="data-buttons">
                    <button
                        class="edit-data-button"
                        data-id="${item.id}"
                    >
                        수정
                    </button>

                    <button
                        class="delete-data-button"
                        data-id="${item.id}"
                    >
                        삭제
                    </button>
                </div>
            `;

            itemElement
                .querySelector(".edit-data-button")
                .addEventListener(
                    "click",
                    () => {
                        startEditData(item);
                    }
                );

            itemElement
                .querySelector(".delete-data-button")
                .addEventListener(
                    "click",
                    () => {
                        deleteData(item.id);
                    }
                );

            dataList.appendChild(itemElement);
        });

    } catch (error) {
        console.error(
            "데이터를 불러오지 못했습니다.",
            error
        );

        dataList.innerHTML =
            '<p class="empty-message">데이터를 불러오지 못했습니다.</p>';
    }
}


// ==============================
// 데이터 추가 / 수정 시작
// ==============================

function startEditData(item) {
    editingDataId = item.id;

    dataDate.value = item.date;
    dataValue.value = item.value;
    dataMemo.value = item.memo || "";

    addDataButton.textContent = "데이터 수정";

    closeMobilePanels();
}


// ==============================
// 데이터 추가
// ==============================

async function addData() {
    const date = dataDate.value;
    const value = dataValue.value;
    const memo = dataMemo.value;

    if (!date || value === "") {
        alert("날짜와 값을 입력해주세요.");
        return;
    }

    if (editingDataId) {
        await updateData(editingDataId);
        return;
    }

    try {
        addDataButton.disabled = true;
        addDataButton.textContent = "추가 중...";

        const response = await fetch(
            `${API_BASE_URL}/api/data`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    date: date,
                    value: Number(value),
                    memo: memo
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                "데이터 추가에 실패했습니다."
            );
        }

        dataDate.value = "";
        dataValue.value = "";
        dataMemo.value = "";

        await loadData();
        await loadSummary();

    } catch (error) {
        console.error(
            "데이터 추가 오류:",
            error
        );

        alert("데이터 추가에 실패했습니다.");

    } finally {
        addDataButton.disabled = false;
        addDataButton.textContent = "데이터 추가";
    }
}


// ==============================
// 데이터 수정
// ==============================

async function updateData(dataId) {
    const date = dataDate.value;
    const value = dataValue.value;
    const memo = dataMemo.value;

    if (!date || value === "") {
        alert("날짜와 값을 입력해주세요.");
        return;
    }

    try {
        addDataButton.disabled = true;
        addDataButton.textContent = "수정 중...";

        const response = await fetch(
            `${API_BASE_URL}/api/data/${dataId}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    date: date,
                    value: Number(value),
                    memo: memo
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                "데이터 수정에 실패했습니다."
            );
        }

        editingDataId = null;

        dataDate.value = "";
        dataValue.value = "";
        dataMemo.value = "";

        await loadData();
        await loadSummary();

    } catch (error) {
        console.error(
            "데이터 수정 오류:",
            error
        );

        alert("데이터 수정에 실패했습니다.");

    } finally {
        addDataButton.disabled = false;
        addDataButton.textContent = "데이터 추가";
    }
}


// ==============================
// 데이터 삭제
// ==============================

async function deleteData(dataId) {
    if (!confirm("이 데이터를 삭제하시겠습니까?")) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/api/data/${dataId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "데이터 삭제에 실패했습니다."
            );
        }

        await loadData();
        await loadSummary();

    } catch (error) {
        console.error(
            "데이터 삭제 오류:",
            error
        );

        alert("데이터 삭제에 실패했습니다.");
    }
}


// ==============================
// 대화 목록 불러오기
// ==============================

async function loadConversations() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/conversations`
        );

        if (!response.ok) {
            throw new Error(
                "대화 목록을 불러오지 못했습니다."
            );
        }

        const conversations =
            await response.json();

        conversationList.innerHTML = "";

        if (conversations.length === 0) {
            conversationList.innerHTML =
                '<p class="empty-message">대화가 없습니다.</p>';
            return;
        }

        conversations.forEach(
            conversation => {
                const item =
                    document.createElement("div");

                item.className =
                    "conversation-item";

                item.textContent =
                    conversation.title;

                item.addEventListener(
                    "click",
                    () => {
                        loadConversation(
                            conversation.id
                        );
                    }
                );

                conversationList.appendChild(item);
            }
        );

    } catch (error) {
        console.error(
            "대화 목록을 불러오지 못했습니다.",
            error
        );
    }
}


// ==============================
// 특정 대화 불러오기
// ==============================

async function loadConversation(
    conversationId
) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/conversations/${conversationId}`
        );

        if (!response.ok) {
            throw new Error(
                "대화를 불러오지 못했습니다."
            );
        }

        const conversation =
            await response.json();

        currentConversationId =
            conversation.id;

        chatMessages.innerHTML = "";

        conversation.messages.forEach(
            message => {
                addMessage(
                    message.role,
                    message.content
                );
            }
        );

        closeMobilePanels();

    } catch (error) {
        console.error(
            "대화를 불러오지 못했습니다.",
            error
        );
    }
}


// ==============================
// 데이터 요약
// ==============================

async function loadSummary() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/data/summary`
        );

        if (!response.ok) {
            throw new Error(
                "요약 정보를 불러오지 못했습니다."
            );
        }

        const summary =
            await response.json();

        if (summary.count === 0) {
            summaryContent.innerHTML =
                "<p>데이터가 없습니다.</p>";
            return;
        }

        summaryContent.innerHTML = `
            <div class="summary-card">
                <strong>기간</strong>
                <span>${summary.period}</span>
            </div>

            <div class="summary-card">
                <strong>데이터 수</strong>
                <span>${summary.count}</span>
            </div>

            <div class="summary-card">
                <strong>평균</strong>
                <span>${summary.metrics.average}</span>
            </div>

            <div class="summary-card">
                <strong>최고</strong>
                <span>${summary.metrics.max}</span>
            </div>

            <div class="summary-card">
                <strong>최저</strong>
                <span>${summary.metrics.min}</span>
            </div>

            <div class="summary-card">
                <strong>추세</strong>
                <span>${summary.trend}</span>
            </div>
        `;

    } catch (error) {
        console.error(
            "요약 정보를 불러오지 못했습니다.",
            error
        );

        summaryContent.innerHTML =
            "<p>요약 정보를 불러오지 못했습니다.</p>";
    }
}


// ==============================
// 메시지 화면에 추가
// ==============================

function addMessage(role, content) {
    const message =
        document.createElement("div");

    message.className =
        `message ${role}`;

    message.textContent = content;

    chatMessages.appendChild(message);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ==============================
// 메시지 전송
// ==============================

async function sendMessage() {
    const message =
        messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(
        "user",
        message
    );

    messageInput.value = "";

    sendButton.disabled = true;
    sendButton.textContent =
        "전송 중...";

    try {
        const response = await fetch(
            `${API_BASE_URL}/api/chat`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id:
                        currentConversationId
                })
            }
        );

        const result =
            await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail ||
                "채팅 요청에 실패했습니다."
            );
        }

        addMessage(
            "assistant",
            result.answer
        );

        currentConversationId =
            result.conversation_id;

        await loadConversations();
        await loadSummary();

    } catch (error) {
        console.error(error);

        addMessage(
            "assistant",
            "오류가 발생했습니다. 서버 연결을 확인해주세요."
        );

    } finally {
        sendButton.disabled = false;
        sendButton.textContent =
            "보내기";
    }
}


// ==============================
// 새 대화
// ==============================

function startNewChat() {
    currentConversationId = null;

    chatMessages.innerHTML = `
        <div class="welcome-message">
            <h2>새로운 대화</h2>
            <p>
                데이터를 바탕으로 궁금한 것을 질문해주세요.
            </p>
        </div>
    `;

    messageInput.value = "";

    closeMobilePanels();
}


// ==============================
// 버튼 이벤트
// ==============================

sendButton.addEventListener(
    "click",
    sendMessage
);

newChatButton.addEventListener(
    "click",
    startNewChat
);

addDataButton.addEventListener(
    "click",
    addData
);


// ==============================
// Enter로 전송
// ==============================

messageInput.addEventListener(
    "keydown",
    event => {
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();
            sendMessage();
        }
    }
);
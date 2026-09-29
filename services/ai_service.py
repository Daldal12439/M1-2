def chat_with_ai(
    openai,
    db,
    message,
    conversation_id,
    summary
):
    # 1. 기존 대화 불러오기

    conversation_messages = []

    if conversation_id:

        conversation_ref = (
            db.collection("conversations")
            .document(conversation_id)
        )

        conversation_doc = conversation_ref.get()

        if conversation_doc.exists:

            conversation_data = (
                conversation_doc.to_dict()
            )

            conversation_messages = (
                conversation_data.get(
                    "messages",
                    []
                )
            )

    # 2. System Prompt

    system_prompt = f"""
너는 사용자의 데이터를 분석하고 질문에 답하는 AI 비서다.

현재 저장된 데이터의 요약 정보는 다음과 같다.

{summary}

이 요약 정보를 참고하여 사용자의 질문에 답변하라.
데이터에 없는 내용은 추측하지 말고, 알 수 없다고 답변하라.
이전 대화 내용이 제공되었다면 그 맥락을 참고하여 자연스럽게 답변하라.
"""

    # 3. GPT에 전달할 메시지 구성

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for conversation_message in conversation_messages:

        messages.append({
            "role": conversation_message["role"],
            "content": conversation_message["content"]
        })

    messages.append({
        "role": "user",
        "content": message
    })

    # 4. OpenAI API 호출

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    # 5. 대화 저장

    if conversation_id:

        conversation_ref = (
            db.collection("conversations")
            .document(conversation_id)
        )

        updated_messages = (
            conversation_messages
            + [
                {
                    "role": "user",
                    "content": message
                },
                {
                    "role": "assistant",
                    "content": answer
                }
            ]
        )

        conversation_ref.update({
            "messages": updated_messages
        })

        saved_conversation_id = conversation_id

    else:

        doc_ref = (
            db.collection("conversations")
            .document()
        )

        messages_to_save = [
            {
                "role": "user",
                "content": message
            },
            {
                "role": "assistant",
                "content": answer
            }
        ]

        doc_ref.set({
            "title": message[:30],
            "messages": messages_to_save
        })

        saved_conversation_id = doc_ref.id

    return {
        "answer": answer,
        "conversation_id": saved_conversation_id
    }
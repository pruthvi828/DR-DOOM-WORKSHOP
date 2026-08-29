from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.chat import conversation_store
from app.main import app
from app.services.groq_chat import GroqChatError

client = TestClient(app)


def test_chat_returns_reply_and_retains_context(monkeypatch) -> None:
    captured_histories: list[list[dict[str, str]]] = []

    def fake_generate_reply(history: list[dict[str, str]], user_text: str) -> str:
        captured_histories.append(history)
        return f"reply to {user_text}"

    monkeypatch.setattr("app.api.chat.generate_reply", fake_generate_reply)
    session_id = uuid4()

    for turn in range(7):
        response = client.post("/api/chat", json={"sessionId": str(session_id), "text": f"message {turn}"})
        assert response.status_code == 200

    body = response.json()
    assert body["sessionId"] == str(session_id)
    assert body["reply"] == "reply to message 6"
    assert body["turnsRetained"] == 6
    assert len(captured_histories[-1]) == 12
    assert captured_histories[-1][0]["content"] == "message 0"

    retained = conversation_store.history(session_id)
    assert len(retained) == 12
    assert retained[0]["content"] == "message 1"
    conversation_store.clear(session_id)


def test_chat_rejects_blank_text() -> None:
    response = client.post("/api/chat", json={"sessionId": str(uuid4()), "text": "   "})

    assert response.status_code == 422


def test_chat_returns_safe_provider_error(monkeypatch) -> None:
    def fake_generate_reply(history: list[dict[str, str]], user_text: str) -> str:
        raise GroqChatError("Groq is not configured.")

    monkeypatch.setattr("app.api.chat.generate_reply", fake_generate_reply)
    response = client.post("/api/chat", json={"sessionId": str(uuid4()), "text": "Hello"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Groq is not configured."

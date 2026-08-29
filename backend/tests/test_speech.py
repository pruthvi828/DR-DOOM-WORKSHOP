from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_lists_curated_voices() -> None:
    response = client.get("/api/voices")

    assert response.status_code == 200
    assert response.json()["voices"][0]["id"] == "en-US-GuyNeural"


def test_tts_returns_mp3(monkeypatch) -> None:
    async def fake_generate_speech(text: str, voice_id: str) -> bytes:
        assert text == "Hello"
        assert voice_id == "en-US-GuyNeural"
        return b"fake-mp3"

    monkeypatch.setattr("app.api.speech.generate_speech", fake_generate_speech)
    response = client.post("/api/tts", json={"text": "Hello", "voiceId": "en-US-GuyNeural"})

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert response.content == b"fake-mp3"


def test_transcribe_valid_webm(monkeypatch) -> None:
    def fake_transcribe(audio: bytes, filename: str, content_type: str) -> str:
        assert audio == b"webm-bytes"
        assert filename == "recording.webm"
        assert content_type == "audio/webm"
        return "Hello Jarvis"

    monkeypatch.setattr("app.api.speech.transcribe", fake_transcribe)
    response = client.post("/api/transcribe", files={"audio": ("recording.webm", b"webm-bytes", "audio/webm")})

    assert response.status_code == 200
    assert response.json() == {"transcript": "Hello Jarvis"}

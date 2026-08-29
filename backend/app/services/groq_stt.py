import io

import requests

from app.settings import settings

GROQ_TRANSCRIBE_URL = "https://api.groq.com/openai/v1/audio/transcriptions"


class GroqSttError(RuntimeError):
    pass


def transcribe(audio: bytes, filename: str, content_type: str) -> str:
    if not settings.groq_api_key:
        raise GroqSttError("Groq is not configured.")
    headers = {"Authorization": f"Bearer {settings.groq_api_key}"}
    files = {
        "file": (filename, io.BytesIO(audio), content_type),
        "model": (None, "whisper-large-v3-turbo"),
        "response_format": (None, "json"),
    }
    try:
        response = requests.post(GROQ_TRANSCRIBE_URL, headers=headers, files=files, timeout=30)
        if not response.ok:
            if response.status_code == 401:
                raise GroqSttError("Groq rejected the configured API key.")
            if response.status_code == 429:
                raise GroqSttError("Groq rate limit reached. Please try again shortly.")
            if response.status_code == 400:
                raise GroqSttError("Recording was too short or unreadable. Hold the button while speaking, then release.")
            raise GroqSttError("Groq could not transcribe that recording.")
        transcript = response.json().get("text", "").strip()
    except GroqSttError:
        raise
    except (requests.RequestException, ValueError, TypeError) as error:
        raise GroqSttError("Speech transcription is currently unavailable.") from error
    return transcript

import requests

from app.settings import settings

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

# ====================================================================
# TODO: [MISSION 2] CRAFT YOUR ASSISTANT'S UNIQUE PERSONALITY CORE
# The SYSTEM_PROMPT defines your AI's persona, tone, and behavioral rules.
#
# PERSONA IDEAS:
# 1. Sarcastic Butler (FRIDAY):
#    "You are Friday, a witty and slightly sarcastic AI assistant. You answer
#     smartly in 2-3 sentences, occasionally making witty remarks about humans."
# 2. Senior Coding Mentor (ATLAS):
#    "You are Atlas, a principal software architect. You give ultra-concise,
#     high-impact technical advice. You never waste words."
# 3. Cyberpunk Hacker (GHOST):
#    "You are Ghost, an underground cyberpunk netrunner. Use subtle slang
#     like 'chummer', 'neural link', and 'grid'. Keep answers sharp."
# ====================================================================
SYSTEM_PROMPT = (
    "You are Jarvis, a concise and helpful web assistant. "
    "Answer directly in plain text, normally within three short sentences. "
    "Do not claim to execute actions, open applications, browse, or access local files."
)


class GroqChatError(RuntimeError):
    def __init__(self, message: str, status_code: int = 503) -> None:
        super().__init__(message)
        self.status_code = status_code


def generate_reply(history: list[dict[str, str]], user_text: str) -> str:
    if not settings.groq_api_key:
        raise GroqChatError("Groq is not configured.")

    # ====================================================================
    # TODO: [MISSION 3] EXPERIMENT WITH TEMPERATURE & TOKEN BOUNDS
    # - temperature: 0.1 (strict/analytical) to 0.8 (creative/witty)
    # - max_completion_tokens: 80 (punchy one-liners) to 250 (detailed)
    # ====================================================================
    payload = {
        "model": settings.groq_chat_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.4,
        "max_completion_tokens": 220,
    }
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(GROQ_CHAT_URL, json=payload, headers=headers, timeout=20)
        if not response.ok:
            error = response.json().get("error", {}) if response.content else {}
            error_code = error.get("code", "")
            if response.status_code == 401:
                raise GroqChatError("Groq rejected the configured API key.")
            if error_code == "model_not_found":
                raise GroqChatError("The configured Groq model is unavailable.")
            if response.status_code == 429:
                raise GroqChatError("Groq rate limit reached. Please try again shortly.")
            raise GroqChatError("Groq could not complete the request.")
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()
    except GroqChatError:
        raise
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
        raise GroqChatError("Jarvis could not get a response from Groq.") from error

    if not reply:
        raise GroqChatError("Jarvis received an empty response from Groq.")
    return reply

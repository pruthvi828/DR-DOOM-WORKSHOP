import json
import re
from typing import Literal
from urllib.parse import quote_plus, urlparse, urlunparse

import requests

from app.settings import settings

# ====================================================================
# TODO: [MISSION 6] ADD YOUR OWN CUSTOM SAFE WEB ACTION!
# Step 1: Add your action name to PlanKind (e.g. "youtube_search", "github_search")
# Step 2: Add keyword detection in _fallback_classification
# Step 3: Format the safe destination URL in make_web_action_plan
# ====================================================================
PlanKind = Literal["web_search"]

PLANNER_PROMPT = """Classify a browser-navigation request. Return JSON only:
{"kind":"web_search","query":"short search text"}.
Use web_search for website/search requests. Never return a URL, command,
file path, app name, or explanation."""


def _explicit_http_url(text: str) -> str | None:
    candidate = re.search(r"(?:https?://)?(?:www\.)?[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+(?:/[^\s]*)?", text, re.IGNORECASE)
    if not candidate:
        return None
    raw = candidate.group(0).rstrip(".,!?)]")
    parsed = urlparse(raw if raw.lower().startswith(("http://", "https://")) else f"https://{raw}")
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        return None
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))


def _fallback_classification(text: str) -> tuple[PlanKind, str]:
    lowered = text.lower()
    query = re.sub(r"\b(?:please|can you|could you|would you|open|launch|start|go to|play|find|search|on|for)\b", " ", text, flags=re.IGNORECASE)
    query = " ".join(query.split()) or text.strip()
    # ====================================================================
    # TODO: [MISSION 6] Add your custom action intent detection here!
    # Example:
    # if "github" in lowered or "git hub" in lowered:
    #     return "github_search", query.replace("GitHub", "").replace("github", "").strip() or "GitHub"
    # ====================================================================
    return "web_search", query


def _model_classification(text: str) -> tuple[PlanKind, str] | None:
    if not settings.groq_api_key:
        return None
    payload = {
        "model": settings.groq_chat_model,
        "messages": [{"role": "system", "content": PLANNER_PROMPT}, {"role": "user", "content": text}],
        "temperature": 0,
        "max_completion_tokens": 120,
        "response_format": {"type": "json_object"},
    }
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {settings.groq_api_key}", "Content-Type": "application/json"},
            timeout=12,
        )
        content = response.json()["choices"][0]["message"]["content"] if response.ok else ""
        parsed = json.loads(content)
        kind = parsed.get("kind")
        query = parsed.get("query")
        if kind in {"web_search"} and isinstance(query, str) and query.strip():
            return kind, query.strip()[:300]
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        pass
    return None


def make_web_action_plan(text: str) -> dict[str, str]:
    explicit_url = _explicit_http_url(text)
    if explicit_url:
        return {"kind": "open_website", "label": urlparse(explicit_url).hostname or "Website", "url": explicit_url}

    kind, query = _model_classification(text) or _fallback_classification(text)
    # ====================================================================
    # TODO: [MISSION 6] Add your custom safe destination URL builders here!
    # Example:
    # if kind == "github_search":
    #     return {"kind": kind, "label": f"GitHub search: {query}", "url": f"https://github.com/search?q={quote_plus(query)}"}
    # ====================================================================
    return {"kind": kind, "label": f"Web search: {query}", "url": f"https://www.google.com/search?q={quote_plus(query)}"}

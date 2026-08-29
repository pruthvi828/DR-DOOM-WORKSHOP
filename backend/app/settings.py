from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend directory or parent workshop root
_current_dir = Path(__file__).resolve().parent
_backend_dir = _current_dir.parent.parent
_workspace_dir = _backend_dir.parent

if (_backend_dir / ".env").is_file():
    load_dotenv(dotenv_path=_backend_dir / ".env")
if (_workspace_dir / ".env").is_file():
    load_dotenv(dotenv_path=_workspace_dir / ".env")
load_dotenv()


def parse_origins(value: str) -> tuple[str, ...]:
    return tuple(origin.strip().rstrip("/") for origin in value.split(",") if origin.strip())


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    backend_host: str = os.getenv("JARVIS_BACKEND_HOST", "127.0.0.1")
    backend_port: int = int(os.getenv("JARVIS_BACKEND_PORT", "8765"))
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_chat_model: str = os.getenv("GROQ_CHAT_MODEL", "openai/gpt-oss-20b")
    allowed_origins: tuple[str, ...] = parse_origins(os.getenv("JARVIS_ALLOWED_ORIGINS", "http://localhost:1420,http://127.0.0.1:1420"))
    local_actions_enabled: bool = parse_bool(os.getenv("JARVIS_LOCAL_ACTIONS_ENABLED", "false"))


settings = Settings()

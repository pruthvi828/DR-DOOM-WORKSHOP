from dataclasses import dataclass
import os
import sys
from typing import Literal

from app.settings import settings

LocalAppId = Literal["calculator", "notepad", "file_explorer", "vscode"]


@dataclass(frozen=True)
class LocalApp:
    app_id: LocalAppId
    label: str
    aliases: tuple[str, ...]
    launch_target: str


# These targets are application-owned constants. User text and model output are
# never used as a program name, path, argument, or shell command.
LOCAL_APPS: tuple[LocalApp, ...] = (
    LocalApp("calculator", "Calculator", ("calculator", "calc"), "ms-calculator:"),
    LocalApp("notepad", "Notepad", ("notepad",), "notepad.exe"),
    LocalApp("file_explorer", "File Explorer", ("file explorer", "explorer"), "explorer.exe"),
    LocalApp("vscode", "Visual Studio Code", ("visual studio code", "vs code", "vscode"), "vscode://"),
)


def local_action_bridge_available() -> bool:
    return settings.local_actions_enabled and settings.backend_host in {"127.0.0.1", "localhost", "::1"} and sys.platform == "win32"


def find_local_app(text: str) -> LocalApp | None:
    normalized = " ".join(text.lower().split())
    for app in LOCAL_APPS:
        if any(alias in normalized for alias in app.aliases):
            return app
    return None


def make_local_action_plan(text: str) -> dict[str, str | bool] | None:
    app = find_local_app(text)
    if not app:
        return None
    return {
        "kind": "open_local_app",
        "app_id": app.app_id,
        "label": app.label,
        "requires_confirmation": True,
    }


def execute_local_action(app_id: LocalAppId) -> LocalApp:
    if not local_action_bridge_available():
        raise RuntimeError("Local actions are disabled or the bridge is not running locally.")

    app = next((item for item in LOCAL_APPS if item.app_id == app_id), None)
    if app is None:
        raise ValueError("That application is not allowlisted.")

    # os.startfile delegates a fixed application/protocol target to Windows.
    # It never receives content from the browser, user, or model.
    os.startfile(app.launch_target)  # type: ignore[attr-defined]
    return app

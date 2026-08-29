from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api import local_actions as local_actions_api
from app.main import app
from app.services import local_actions

client = TestClient(app)


def enable_local_actions(monkeypatch) -> None:
    monkeypatch.setattr(local_actions, "settings", SimpleNamespace(local_actions_enabled=True, backend_host="127.0.0.1"))
    monkeypatch.setattr(local_actions.sys, "platform", "win32")


def test_local_planner_returns_only_allowlisted_app() -> None:
    plan = local_actions.make_local_action_plan("Please open Calculator")

    assert plan == {
        "kind": "open_local_app",
        "app_id": "calculator",
        "label": "Calculator",
        "requires_confirmation": True,
    }


def test_local_planner_rejects_unknown_app() -> None:
    assert local_actions.make_local_action_plan("Open a random executable") is None


def test_execute_uses_fixed_allowlisted_target(monkeypatch) -> None:
    enable_local_actions(monkeypatch)
    launched: list[str] = []
    monkeypatch.setattr(local_actions.os, "startfile", lambda target: launched.append(target), raising=False)

    app_definition = local_actions.execute_local_action("calculator")

    assert app_definition.label == "Calculator"
    assert launched == ["ms-calculator:"]


def test_execute_is_blocked_when_local_bridge_disabled(monkeypatch) -> None:
    monkeypatch.setattr(local_actions, "settings", SimpleNamespace(local_actions_enabled=False, backend_host="127.0.0.1"))

    try:
        local_actions.execute_local_action("notepad")
    except RuntimeError as error:
        assert "disabled" in str(error)
    else:
        raise AssertionError("Disabled local bridge must reject execution")


def test_local_action_api_requires_confirmation_and_uses_safe_response(monkeypatch) -> None:
    monkeypatch.setattr(local_actions_api, "local_action_bridge_available", lambda: True)
    response = client.post("/api/local-actions/plan", json={"text": "open Notepad"})

    assert response.status_code == 200
    assert response.json() == {
        "kind": "open_local_app",
        "appId": "notepad",
        "label": "Notepad",
        "requiresConfirmation": True,
    }

    rejected = client.post("/api/local-actions/execute", json={"appId": "notepad", "confirmed": False})
    assert rejected.status_code == 422


def test_local_action_api_rejects_public_browser_origin(monkeypatch) -> None:
    monkeypatch.setattr(local_actions_api, "local_action_bridge_available", lambda: True)

    response = client.post(
        "/api/local-actions/plan",
        json={"text": "open Notepad"},
        headers={"Origin": "https://jarvis.example"},
    )

    assert response.status_code == 403

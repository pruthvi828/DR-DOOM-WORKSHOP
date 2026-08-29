from fastapi.testclient import TestClient

from app.main import app
from app.services.web_action_planner import make_web_action_plan

client = TestClient(app)


def test_direct_website_plan_uses_only_user_http_url() -> None:
    plan = make_web_action_plan("Please open https://example.org/products?tag=jarvis")
    assert plan == {
        "kind": "open_website",
        "label": "example.org",
        "url": "https://example.org/products?tag=jarvis",
    }


def test_web_action_endpoint_returns_constrained_plan(monkeypatch) -> None:
    monkeypatch.setattr("app.services.web_action_planner._model_classification", lambda _: None)
    response = client.post("/api/web-actions/plan", json={"text": "open the official NASA website"})
    assert response.status_code == 200
    body = response.json()
    assert body["kind"] == "web_search"
    assert body["url"].startswith("https://www.google.com/search?q=")

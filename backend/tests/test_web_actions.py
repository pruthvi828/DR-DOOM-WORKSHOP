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


def test_youtube_plan_uses_generated_search_url(monkeypatch) -> None:
    monkeypatch.setattr("app.services.web_action_planner._model_classification", lambda _: None)
    plan = make_web_action_plan("Play lofi coding music on YouTube")
    assert plan["kind"] == "youtube_search"
    assert plan["url"] == "https://www.youtube.com/results?search_query=lofi+coding+music"


def test_web_action_endpoint_returns_constrained_plan(monkeypatch) -> None:
    monkeypatch.setattr("app.services.web_action_planner._model_classification", lambda _: None)
    response = client.post("/api/web-actions/plan", json={"text": "open the official NASA website"})
    assert response.status_code == 200
    body = response.json()
    assert body["kind"] == "web_search"
    assert body["url"].startswith("https://www.google.com/search?q=")


def test_github_plan_uses_generated_search_url(monkeypatch) -> None:
    monkeypatch.setattr("app.services.web_action_planner._model_classification", lambda _: None)
    plan = make_web_action_plan("search github for fast visualizers")
    assert plan["kind"] == "github_search"
    assert plan["url"] == "https://github.com/search?q=fast+visualizers"

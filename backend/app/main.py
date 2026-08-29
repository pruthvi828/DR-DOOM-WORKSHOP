from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.local_actions import router as local_actions_router
from app.api.speech import router as speech_router
from app.api.web_actions import router as web_actions_router
from app.settings import settings

app = FastAPI(title="Jarvis Backend", version="0.1.0")

# Web deployments must provide JARVIS_ALLOWED_ORIGINS with their exact frontend
# URL(s). Wildcard CORS is intentionally never enabled.
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(chat_router)
app.include_router(local_actions_router)
app.include_router(speech_router)
app.include_router(web_actions_router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

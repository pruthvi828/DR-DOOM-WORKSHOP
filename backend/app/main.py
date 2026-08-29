from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import requests
from app.settings import settings

app = FastAPI(title="Jarvis Starter Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=128)
    message: str = Field(..., min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    reply: str
    session_id: str

@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    if not settings.groq_api_key:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY is not configured in .env file.")
    
    # Direct Groq LLM API Call for Mission 0
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.groq_chat_model,
        "messages": [
            {"role": "user", "content": payload.message}
        ],
        "temperature": 0.5,
        "max_completion_tokens": 150,
    }
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers, timeout=12)
        if not res.ok:
            raise HTTPException(status_code=500, detail=f"Groq API Error: {res.text}")
        reply_text = res.json()["choices"][0]["message"]["content"]
        return ChatResponse(reply=reply_text, session_id=payload.session_id)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

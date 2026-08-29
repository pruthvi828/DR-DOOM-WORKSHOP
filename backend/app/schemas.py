from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: UUID = Field(alias="sessionId")
    text: str = Field(min_length=1, max_length=2_000)


class ChatResponse(BaseModel):
    session_id: UUID = Field(alias="sessionId")
    reply: str
    turns_retained: int = Field(alias="turnsRetained", ge=0, le=6)


class Voice(BaseModel):
    id: str
    label: str


class VoicesResponse(BaseModel):
    voices: list[Voice]


class TtsRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)
    voice_id: str = Field(alias="voiceId")


class TranscriptResponse(BaseModel):
    transcript: str


class WebActionPlanRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)


class WebActionPlanResponse(BaseModel):
    kind: Literal["open_website", "web_search", "youtube_search", "spotify_search", "github_search"]
    label: str = Field(min_length=1, max_length=160)
    url: str = Field(min_length=1, max_length=2_000)


class LocalActionPlanRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)


class LocalActionPlanResponse(BaseModel):
    kind: Literal["open_local_app"]
    app_id: Literal["calculator", "notepad", "file_explorer", "vscode"] = Field(alias="appId")
    label: str = Field(min_length=1, max_length=160)
    requires_confirmation: bool = Field(alias="requiresConfirmation")


class LocalActionExecuteRequest(BaseModel):
    app_id: Literal["calculator", "notepad", "file_explorer", "vscode"] = Field(alias="appId")
    confirmed: Literal[True]


class LocalActionExecuteResponse(BaseModel):
    ok: bool
    message: str


class LocalActionStatusResponse(BaseModel):
    enabled: bool

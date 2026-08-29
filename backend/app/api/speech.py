import asyncio

from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status

from app.schemas import TranscriptResponse, TtsRequest, VoicesResponse
from app.services.edge_tts_service import EdgeTtsError, available_voices, generate_speech
from app.services.groq_stt import GroqSttError, transcribe

router = APIRouter(prefix="/api", tags=["speech"])
ALLOWED_AUDIO_TYPES = {"audio/webm", "audio/ogg", "audio/wav", "audio/mp4", "audio/mpeg"}
MAX_AUDIO_BYTES = 10 * 1024 * 1024


@router.get("/voices", response_model=VoicesResponse)
async def voices() -> VoicesResponse:
    return VoicesResponse(voices=available_voices())


@router.post("/tts", response_class=Response)
async def tts(request: TtsRequest) -> Response:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Text cannot be blank.")
    try:
        audio = await generate_speech(text, request.voice_id)
    except EdgeTtsError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return Response(content=audio, media_type="audio/mpeg")


@router.post("/transcribe", response_model=TranscriptResponse)
async def transcribe_audio(audio: UploadFile = File(...)) -> TranscriptResponse:
    content_type = audio.content_type or ""
    if content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported audio format.")
    payload = await audio.read()
    if not payload:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Audio recording is empty.")
    if len(payload) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Audio recording is too large.")
    try:
        transcript = await asyncio.to_thread(transcribe, payload, audio.filename or "recording.webm", content_type)
    except GroqSttError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return TranscriptResponse(transcript=transcript)

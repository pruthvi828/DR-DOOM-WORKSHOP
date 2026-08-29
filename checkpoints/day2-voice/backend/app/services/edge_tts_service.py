import edge_tts

from app.schemas import Voice

# ====================================================================
# TODO: [MISSION 5] EXPAND YOUR ASSISTANT'S NEURAL VOICE CATALOG
# Edge TTS supports high-fidelity voices across multiple accents.
# Add your favorite voices to this tuple!
#
# POPULAR REGIONAL VOICES:
# - Voice(id="en-GB-SoniaNeural", label="Sonia — UK English (Sophisticated)")
# - Voice(id="en-AU-NatashaNeural", label="Natasha — Australian English")
# - Voice(id="en-IN-NeerjaNeural", label="Neerja — Indian English (Expressive)")
# - Voice(id="en-IN-PrabhatNeural", label="Prabhat — Indian English (Male)")
# - Voice(id="en-US-ChristopherNeural", label="Christopher — US English (Calm)")
# - Voice(id="en-CA-LiamNeural", label="Liam — Canadian English")
# ====================================================================
VOICES = (
    Voice(id="en-US-GuyNeural", label="Guy — US English"),
    Voice(id="en-GB-RyanNeural", label="Ryan — UK English"),
    Voice(id="en-US-JennyNeural", label="Jenny — US English"),
    Voice(id="en-GB-SoniaNeural", label="Sonia — UK English (Sophisticated)"),
    Voice(id="en-IN-NeerjaNeural", label="Neerja — Indian English"),
)
VOICE_IDS = {voice.id for voice in VOICES}


class EdgeTtsError(RuntimeError):
    pass


def available_voices() -> list[Voice]:
    return list(VOICES)


async def generate_speech(text: str, voice_id: str) -> bytes:
    if voice_id not in VOICE_IDS:
        raise EdgeTtsError("The selected voice is unavailable.")

    audio = bytearray()
    try:
        stream = edge_tts.Communicate(text=text, voice=voice_id)
        async for chunk in stream.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
    except Exception as error:
        raise EdgeTtsError("Speech generation is currently unavailable.") from error

    if not audio:
        raise EdgeTtsError("Speech generation returned no audio.")
    return bytes(audio)

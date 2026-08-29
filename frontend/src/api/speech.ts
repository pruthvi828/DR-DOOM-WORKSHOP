export type Voice = { id: string; label: string };
import { API_BASE_URL } from "./client";

export async function fetchVoices(): Promise<Voice[]> {
  const response = await fetch(`${API_BASE_URL}/voices`);
  if (!response.ok) throw new Error("Voice options are unavailable.");
  const body = await response.json() as { voices: Voice[] };
  return body.voices;
}

export async function requestSpeech(text: string, voiceId: string): Promise<Blob> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, voiceId }),
    });
  } catch {
    throw new Error("Speech service is unavailable.");
  }
  if (!response.ok) throw new Error("Speech generation is unavailable. The text reply is still available.");
  return response.blob();
}

export async function transcribeRecording(audio: Blob): Promise<string> {
  const form = new FormData();
  form.append("audio", audio, "recording.webm");
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/transcribe`, { method: "POST", body: form });
  } catch {
    throw new Error("Speech transcription service is unavailable.");
  }
  if (!response.ok) {
    const body: { detail?: string } = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "Jarvis could not transcribe that recording.");
  }
  return (await response.json() as { transcript: string }).transcript;
}

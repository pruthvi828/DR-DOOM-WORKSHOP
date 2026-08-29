export type ChatResponse = {
  sessionId: string;
  reply: string;
  turnsRetained: number;
};
import { API_BASE_URL } from "./client";

export async function sendChatMessage(sessionId: string, text: string): Promise<ChatResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessionId, text }),
    });
  } catch {
    throw new Error("Jarvis service is unavailable. Please try again shortly.");
  }

  if (!response.ok) {
    const body: { detail?: string } = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "Jarvis could not process that message.");
  }

  return response.json() as Promise<ChatResponse>;
}

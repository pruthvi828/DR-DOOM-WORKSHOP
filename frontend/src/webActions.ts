import { API_BASE_URL } from "./api/client";

export type WebAction = {
  kind: "open_website" | "web_search";
  label: string;
  url: string;
};

export function isWebActionRequest(text: string): boolean {
  return /\b(open|launch|start|go to|play|find|search)\b/i.test(text);
}

export async function planWebAction(text: string): Promise<WebAction> {
  const response = await fetch(`${API_BASE_URL}/web-actions/plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Jarvis could not prepare that web action.");
  return response.json() as Promise<WebAction>;
}

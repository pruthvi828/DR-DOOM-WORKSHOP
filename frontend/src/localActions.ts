import { API_BASE_URL } from "./api/client";

export type LocalAction = {
  kind: "open_local_app";
  appId: "calculator" | "notepad" | "file_explorer" | "vscode";
  label: string;
  requiresConfirmation: true;
};

const localAppPattern = /\b(calculator|calc|notepad|file explorer|explorer|visual studio code|vs code|vscode)\b/i;
const launchPattern = /\b(open|launch|start)\b/i;

export function isLocalActionRequest(text: string): boolean {
  return launchPattern.test(text) && localAppPattern.test(text);
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (response.ok) return response.json() as Promise<T>;
  const body = await response.json().catch(() => null) as { detail?: string } | null;
  throw new Error(body?.detail || "Jarvis could not complete that local action.");
}

export async function getLocalActionStatus(): Promise<boolean> {
  const status = await requestJson<{ enabled: boolean }>("/local-actions/status");
  return status.enabled;
}

export function planLocalAction(text: string): Promise<LocalAction> {
  return requestJson<LocalAction>("/local-actions/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export function executeLocalAction(appId: LocalAction["appId"]): Promise<{ ok: true; message: string }> {
  return requestJson<{ ok: true; message: string }>("/local-actions/execute", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ appId, confirmed: true }),
  });
}

import { API_BASE_URL } from "./client";

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

export async function waitForBackend(attempts = 30, delayMs = 500): Promise<boolean> {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await checkBackendHealth()) return true;
    await new Promise<void>((resolve) => window.setTimeout(resolve, delayMs));
  }
  return false;
}

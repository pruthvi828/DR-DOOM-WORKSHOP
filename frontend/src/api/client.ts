const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

// Local Vite development uses its proxy. A deployed frontend supplies this at
// build time, for example https://jarvis-api.example.com/api.
export const API_BASE_URL = configuredBaseUrl || "/api";

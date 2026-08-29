# Jarvis frontend

The frontend is a React 19 + Vite application. It owns the visual interface, microphone capture, audio playback, browser navigation after confirmation, and local-only movable panel positions.

## Prerequisites

- Node.js 20 or newer
- The Jarvis backend running at `http://127.0.0.1:8765` for local development

## Install and run

```powershell
cd app/frontend
npm install
npm run dev
```

Vite listens on `http://localhost:1420`. Its development proxy forwards `/api` calls to the local FastAPI backend.

## Environment

Copy `.env.example` to `.env` only when you need to override the API location:

```text
VITE_API_BASE_URL=https://your-api.example/api
```

The value is public build configuration, never a secret. Leave it unset for local development; Vite's proxy will be used.

## Commands

```powershell
npm run lint    # Type-check frontend source without output files
npm run build   # Type-check and create dist/ production assets
npm run preview # Serve an existing production build locally
```

`dist/` and TypeScript cache files are generated artifacts and are intentionally not committed.

## Responsibilities

- Captures text and microphone audio; stops streams and animation loops immediately after use.
- Displays API/service states with an accessible text fallback if speech is unavailable.
- Opens browser destinations only inside a direct user confirmation click.
- Stores only panel positions in the browser's local storage. It does not persist chat history or recordings.

For API contracts, see [the backend guide](../backend/README.md).

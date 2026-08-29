# Jarvis workshop guide

## Goal

Participants finish with a browser-based voice assistant: text chat, push-to-talk, speech transcription, selectable speech output, safe web actions, and a lightweight animated interface.

## Suggested two-day sequence

### Day 1 — working assistant

1. Explain the browser/frontend/backend boundary and create the Groq key locally in `backend/.env`.
2. Run the FastAPI health route and Vite development server.
3. Trace text chat from React to FastAPI to Groq and back.
4. Add or inspect the six-turn in-memory conversation store.
5. Test microphone capture, Groq Whisper transcription, and Edge TTS; demonstrate that text still works if microphone permission is denied.

### Day 2 — safe actions and interface

1. Build the browser action planner and explain why the model cannot provide arbitrary URLs or commands.
2. Add the user confirmation control before opening a new tab.
3. Explore the HUD: CSS video background, Web Audio level signal, movable panels, and the orb push-to-talk control.
4. Optionally demonstrate the disabled-by-default local bridge and its fixed Windows allowlist.
5. Run the verification commands and discuss deployment CORS configuration.

## Separating this monorepo after the workshop

The folders are intentionally self-contained:

1. Create the **jarvis-frontend** repository from `app/frontend`. Keep its `README.md`, `package.json`, `src/`, `index.html`, Vite config, and lockfile.
2. Create the **jarvis-backend** repository from `app/backend`. Keep its `README.md`, `requirements.txt`, `run-dev.ps1`, `app/`, `tests/`, and `.env.example`; never copy `.env`, `.venv`, caches, builds, or distribution folders.
3. Give the frontend its deployed `VITE_API_BASE_URL` during its build. Configure the backend's `JARVIS_ALLOWED_ORIGINS` with that exact frontend origin.
4. Keep the local-app bridge disabled on publicly deployed backend instances.

The root repository remains useful as the workshop bundle because it contains both services, this guide, the design context, and the durable progress record.

## Manual acceptance checks

- Text conversation receives a reply with a valid Groq key.
- A held microphone recording transcribes; denial still leaves text input usable.
- TTS responds with selected voice audio.
- Website/search request shows a generated destination, then only opens after clicking confirmation.
- Right-click a panel or orb, select Move, drag it, then select Fix position.
- With the local bridge disabled, no local apps can launch. If deliberately enabled on a local Windows machine, only the four documented allowlisted applications can launch after confirmation.

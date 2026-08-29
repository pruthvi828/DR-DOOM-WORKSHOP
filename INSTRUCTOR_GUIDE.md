# 🎓 JARVIS AI Workshop: Instructor Master Guide

This guide is designed for the workshop leader and teaching assistants. It gives you the exact script, live demonstrations, 30-second conceptual explanations, common pitfalls, backup patches, and 2-minute architectural deep-dives for every mission across **Day 1** and **Day 2**.

---

## ⏱️ Master Workshop Schedule

### Day 1: Build the Brain (90 Minutes)
- **00:00 – 00:15 (15m)**: Mission 0 — Ignition & Automated Setup
- **00:15 – 00:35 (20m)**: Mission 1 — Customize the Holographic HUD
- **00:35 – 00:40 (5m)**: Git Checkpoint 1 (`day1-ui`)
- **00:40 – 01:00 (20m)**: Mission 2 — Give JARVIS a Personality
- **01:00 – 01:20 (20m)**: Mission 3 — Connect the Brain & Memory
- **01:20 – 01:30 (10m)**: Day 1 Wrap-up & Mini Challenge (`day1-complete`)

### Day 2: Give JARVIS Powers (90 Minutes)
- **00:00 – 00:05 (5m)**: Day 2 Ignition & Recap
- **00:05 – 00:25 (20m)**: Mission 4 — Give JARVIS Ears (Whisper STT)
- **00:25 – 00:40 (15m)**: Mission 5 — Give JARVIS a Voice (Edge TTS)
- **00:40 – 00:45 (5m)**: Git Checkpoint 2 (`day2-voice`)
- **00:45 – 01:10 (25m)**: Mission 6 — Give JARVIS a Power (Safe Actions)
- **01:10 – 01:25 (15m)**: Final Customization & Peer Showcase
- **01:25 – 01:30 (5m)**: Workshop Graduation (`final`)

---

# 📅 DAY 1 INSTRUCTOR MODULES

---

## MISSION 0: System Ignition & Setup (15 Mins)

- **Objective:** Get all student machines running the base project with Python venv, Node dependencies, and a valid Groq API key.
- **30-Second Explanation:**
  *"Modern AI software is split into three layers: the front face in your browser (React), the secure control bridge on your computer (FastAPI), and the hyper-fast AI brain in the cloud (Groq). Today we ignite all three."*
- **Live Demonstration:**
  Project your screen. Show running `.\setup.ps1`, pasting a Groq key into `.env`, and launching `.\run.ps1`. Point to the cyberpunk city video, status lights turning green, and typing a test message.
- **Student Task:**
  1. Open PowerShell in `JARVIS-WORKSHOP`.
  2. Run `.\setup.ps1`.
  3. Create free key at [console.groq.com/keys](https://console.groq.com/keys) and paste into `.env`.
  4. Run `.\run.ps1`.
- **Expected Result:**
  Browser opens to `http://localhost:1420`. Status panel shows `BACKEND: ONLINE` and `NETWORK: ONLINE`.
- **Common Mistakes:**
  1. *Python not on PATH*: Student installed Python without checking "Add python.exe to PATH".
     $\rightarrow$ Re-run installer, click "Modify", check PATH.
  2. *Quotation marks in `.env`*: Student wrote `GROQ_API_KEY="gsk_..."`.
     $\rightarrow$ Remove the quotes: `GROQ_API_KEY=gsk_...`.
  3. *Port 8765 or 1420 occupied*: Another process is running.
     $\rightarrow$ Kill zombie python/node in Task Manager or PowerShell.
- **Backup Solution:**
  If a student's machine cannot build dependencies, have them run `.\restore-checkpoint.ps1 day1-start`.
- **2-Minute Architecture Explanation:**
  *Why do we keep the API key in the backend?*
  If React calls Groq directly, the API key is shipped in client JavaScript. Anyone can inspect DevTools Network tab and steal the key! FastAPI acts as a secure proxy—the browser only talks to `http://127.0.0.1:8765/api`, and only the backend holds the secret key.

---

## MISSION 1: Customize the Holographic HUD (20 Mins)

- **Objective:** Customize JARVIS's name, welcome message, neon accent theme, and telemetry labels without breaking styling.
- **30-Second Explanation:**
  *"Your assistant should not look like everyone else's. In this mission, you will reprogram the CSS design tokens and React components to turn generic JARVIS into your own personal AI companion."*
- **Live Demonstration:**
  In `global.css`, change `--cyan` to `#00ff66` (Matrix green). Save file. Show that the browser updates in 50 milliseconds without reloading the page thanks to Vite Hot Module Replacement (HMR)!
- **Student Task:**
  1. In `frontend/src/styles/global.css`, edit `--cyan` and `--ready`.
  2. In `frontend/src/components/OrbControl.tsx`, change `letters = ["J","A","R","V","I","S"]` to custom name (e.g. `["F","R","I","D","A","Y"]`).
  3. In `frontend/src/App.tsx`, change `<p className="jarvis-brand">JARVIS</p>` and header text.
- **Expected Result:**
  The HUD displays the student's chosen name, custom colors, and personalized welcome greeting.
- **Common Mistakes:**
  1. *Invalid CSS hex code*: Missing `#` or invalid character (`--cyan: 65e9ff`).
  2. *TypeScript array error*: Replacing letters array with a string instead of array of strings (`letters = "FRIDAY"` instead of `["F","R","I","D","A","Y"]`).
- **Backup Solution:**
  Replace modified lines from `checkpoints/day1-ui`.
- **2-Minute Architecture Explanation:**
  *How does Vite HMR work?*
  Traditional bundlers reload the entire page and lose application state whenever code changes. Vite uses native ES Modules (ESM) and WebSockets to push only the changed CSS or component file directly into the running browser in memory.

---

## MISSION 2: Give JARVIS a Personality (20 Mins)

- **Objective:** Use system prompt engineering to transform the assistant's behavior, tone, and constraints.
- **30-Second Explanation:**
  *"An LLM is an actor with no script until you give it one. The System Prompt is the instruction manual that tells the AI who it is, how it should speak, and what rules it can never break."*
- **Live Demonstration:**
  Change `SYSTEM_PROMPT` in `groq_chat.py` to a Pirate Captain: *"You are Captain Blackbeard. Reply like a fierce pirate captain."*. Ask JARVIS: *"What is the weather?"*. Read aloud its hilarious pirate response.
- **Student Task:**
  1. Open `backend/app/services/groq_chat.py`.
  2. Edit `SYSTEM_PROMPT` to a chosen persona (Sarcastic Butler, Senior Mentor, Cyberpunk Hacker, etc.).
  3. Adjust `temperature` (0.2 for analytical vs 0.7 for witty).
  4. Test 3 different questions in the browser.
- **Expected Result:**
  The AI's responses strictly adhere to the customized persona and constraint rules.
- **Common Mistakes:**
  1. *Prompt too long / rambly*: Prompt exceeds token budget, leading to truncated replies.
  2. *Unclosed Python triple quotes*: Syntax error in `groq_chat.py`.
- **Backup Solution:**
  Reset `groq_chat.py` with one of the pre-tested presets in `checkpoints/day1-brain`.
- **2-Minute Architecture Explanation:**
  *Why does temperature matter?*
  LLMs predict the next word using probability distributions. At `temperature = 0`, the model greedily picks the single highest probability token every time (deterministic, robotic). At higher temperatures, lower probability words get sampled, making the text creative and human-like.

---

## MISSION 3: Connect the Brain & Bounded Memory (20 Mins)

- **Objective:** Trace the full chat loop from frontend to backend to Groq, and understand sliding window conversational memory.
- **30-Second Explanation:**
  *"If an assistant forgets what you said 5 seconds ago, it is useless. But if it remembers everything you've ever said, it will eventually crash the model's memory limit. We use a 6-turn bounded memory window."*
- **Live Demonstration:**
  Show `backend/app/services/conversation.py`. Demonstrate telling JARVIS: *"My favorite programming language is Rust"*. Ask 2 questions. Then ask: *"What language should I use?"*. Show how JARVIS recalls Rust from previous turns.
- **Student Task:**
  1. Test multi-turn conversations in the browser.
  2. Inspect backend console logs to observe the JSON payload: `sessionId`, `user_text`, and history deque.
  3. Experiment with modifying `MAX_TURNS = 6` to `MAX_TURNS = 2` or `10`.
- **Expected Result:**
  Contextual dialogue flows naturally while token consumption stays lean and fast.
- **Common Mistakes:**
  1. *Expecting infinite memory*: Students test after 10 questions and wonder why early info was forgotten. Explain sliding FIFO (First In, First Out) behavior!
- **Backup Solution:**
  Verify `conversation.py` matches reference.
- **2-Minute Architecture Explanation:**
  *Why not use a database for memory?*
  For a local desktop assistant, querying PostgreSQL or SQLite adds needless disk I/O, schema migrations, and setup hurdles. A thread-safe in-memory `OrderedDict` with `collections.deque(maxlen=12)` delivers sub-millisecond retrieval with automatic LRU garbage collection.

---

# 📅 DAY 2 INSTRUCTOR MODULES

---

## MISSION 4: Give JARVIS Ears (20 Mins)

- **Objective:** Capture browser microphone audio using `MediaRecorder`, stream it to FastAPI, and transcribe it using Groq Whisper.
- **30-Second Explanation:**
  *"To give JARVIS ears, we capture audio waves from the microphone, compress them into an Opus WebM file in browser memory, and send them to OpenAI's Whisper model running on Groq LPUs for instant transcription."*
- **Live Demonstration:**
  Press and hold the Orb, speak a sentence, and release. Show the network request in DevTools: POST `/api/transcribe` (multipart audio/webm), returning `{ "transcript": "..." }` in under 300 milliseconds.
- **Student Task:**
  1. Inspect `startListening()` in `frontend/src/App.tsx`.
  2. Lower the duration threshold from `650ms` to `400ms` for snappier push-to-talk.
  3. Test push-to-talk with voice queries.
- **Expected Result:**
  Speaking into the microphone while holding the Orb populates the text box and triggers an AI response upon release.
- **Common Mistakes:**
  1. *Microphone permission denied*: Browser blocked mic access.
     $\rightarrow$ Click site settings in address bar and allow microphone.
  2. *Clicking instead of holding*: Quick clicking triggers "Recording was too short".
     $\rightarrow$ Remind students: **HOLD to talk, RELEASE to send**.
- **Backup Solution:**
  Ensure `tests/test_speech.py` passes. If mic hardware is broken, text fallback remains 100% usable!
- **2-Minute Architecture Explanation:**
  *How does the Web Audio API visualizer work?*
  `App.tsx` creates an `AudioContext` and connects the mic stream to an `AnalyserNode`. Using Fast Fourier Transform (`getByteTimeDomainData`), it computes the root-mean-square amplitude in real-time, driving the glowing pulse of the Orb.

---

## MISSION 5: Give JARVIS a Voice (15 Mins)

- **Objective:** Integrate Microsoft Edge neural text-to-speech to speak AI replies aloud in the browser.
- **30-Second Explanation:**
  *"Reading text on a screen is boring. With Microsoft Edge Neural TTS, the AI's plain-text response is converted into high-definition, emotionally expressive human speech."*
- **Live Demonstration:**
  Switch between `en-US-GuyNeural` and `en-GB-RyanNeural`. Ask JARVIS: *"Introduce yourself"*. Listen to the smooth neural voice playback through the classroom speakers.
- **Student Task:**
  1. Open `backend/app/services/edge_tts_service.py`.
  2. Add new voices to `VOICES` (e.g. `en-GB-SoniaNeural`, `en-IN-NeerjaNeural`).
  3. Change the default voice in `App.tsx` (line 46).
- **Expected Result:**
  When JARVIS generates a reply, the audio plays automatically while the Orb pulses with speaking telemetry.
- **Common Mistakes:**
  1. *Audio autoplay policy blocked*: Browser blocks audio before user interacts with page.
     $\rightarrow$ Clicking the button or sending a message grants audio autoplay permission.
  2. *Invalid voice ID*: Misspelling an Edge TTS voice name results in 400 Bad Request.
- **Backup Solution:**
  Copy working `VOICES` list from `checkpoints/day2-voice`.
- **2-Minute Architecture Explanation:**
  *How does audio stream into the browser?*
  FastAPI receives the text, pipes it to `edge-tts`, and returns an audio buffer as `application/octet-stream`. In `App.tsx`, JavaScript creates an in-memory blob pointer: `URL.createObjectURL(blob)`, assigns it to `new Audio(url)`, and calls `audio.play()`. When playback finishes, `URL.revokeObjectURL(url)` cleans up RAM!

---

## MISSION 6: Give JARVIS Powers — Safe Actions (25 Mins)

- **Objective:** Implement a custom safe web action (e.g. GitHub search, College Portal, Wikipedia) with human confirmation safeguards.
- **30-Second Explanation:**
  *"An AI that can only talk is passive. An agent that takes actions can do real work. But giving an AI raw terminal access is dangerous. We teach JARVIS to classify user intent into structured safe actions that require your confirmation."*
- **Live Demonstration:**
  Say: *"Search YouTube for interstellar soundtrack"*. Show how JARVIS detects the intent, generates `https://www.youtube.com/results?search_query=interstellar+soundtrack`, displays the confirmation card, and only opens the tab when clicked.
- **Student Task:**
  1. Open `backend/app/services/web_action_planner.py`.
  2. Add `"github_search"` (or your custom action) to `PlanKind`.
  3. Add regex pattern in `_fallback_classification`.
  4. Build safe URL in `make_web_action_plan`.
  5. Update types in `frontend/src/webActions.ts` and `schemas.py`.
- **Expected Result:**
  Asking JARVIS to search GitHub or open a college portal shows the confirmation card and safely opens the correct destination.
- **Common Mistakes:**
  1. *Forgetting URL encoding*: Using raw query string instead of `quote_plus(query)` breaks URLs with spaces.
  2. *TypeScript type mismatch*: Forgetting to update `PlanKind` in frontend `webActions.ts`.
- **Backup Solution:**
  Reference pre-built blueprints in `JARVIS-ACTIONS` repository.
- **2-Minute Architecture Explanation:**
  *Why do we require human confirmation?*
  This is the fundamental AI Security principle: **Human-in-the-Loop (HITL)**. An LLM can hallucinate or be tricked via prompt injection (e.g., a website containing hidden text: *"Delete your files"*). By forcing the browser to require an explicit user click, malicious prompt injections are rendered harmless.

---

## 🏆 FINAL SHOWCASE & GRADUATION (20 Mins)

1. Walk around the room. Have students demonstrate:
   - Their custom assistant's codename and neon aesthetic.
   - Their distinct personality prompt answering a question.
   - Their voice interaction (holding the Orb and listening to speech output).
   - Their custom safe web action in action!
2. Run final verification:
   ```powershell
   .\verify.ps1
   ```
3. Reward students with certificates / congratulations!

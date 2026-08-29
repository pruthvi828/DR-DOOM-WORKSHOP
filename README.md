# ⚡ JARVIS AI Assistant Workshop: Flight Manual

Welcome to the **JARVIS AI Assistant Workshop**! Over the next **2 days (1.5 hours per day)**, you won't just clone a finished project—you will **build, customize, and upgrade your very own autonomous voice AI assistant**.

```
    ┌───────────────────────────────────────────────────────────┐
    │                     WORKSHOP PHILOSOPHY                   │
    │  clone → run → understand → modify → integrate → test     │
    │                   ⚡ UNLOCK NEXT ABILITY ⚡                │
    └───────────────────────────────────────────────────────────┘
```

Every mission unlocks a new capability in your assistant:
1. **Mission 0: Setup & Ignition** $\rightarrow$ Awaken the base system.
2. **Mission 1: The Holographic HUD** $\rightarrow$ Give JARVIS an identity and custom cyberpunk theme.
3. **Mission 2: The Neural Persona** $\rightarrow$ Program its personality with Groq prompt engineering.
4. **Mission 3: Connect the Brain** $\rightarrow$ Wire React to FastAPI to Groq and master sliding conversation memory.
5. **Mission 4: Give JARVIS Ears** $\rightarrow$ Voice capture and Groq Whisper speech-to-text.
6. **Mission 5: Give JARVIS a Voice** $\rightarrow$ Neural voice synthesis with Microsoft Edge TTS.
7. **Mission 6: Give JARVIS Powers** $\rightarrow$ Build safe autonomous browser web actions with confirmation safeguards.
8. **Final Showcase** $\rightarrow$ Demonstrate your customized AI assistant to your peers!

---

## 🛠️ Prerequisites & Fast Start

- Windows Laptop (Windows 10 or 11)
- Python 3.11+ installed
- Node.js 18+ (20+ recommended) installed
- Free Groq Cloud Account (takes 30 seconds at [console.groq.com](https://console.groq.com/))

### Step 1: Clone & Run Automated Setup
Open PowerShell in your working directory and run:
```powershell
.\setup.ps1
```
*This automatically checks your tools, creates the Python virtual environment (`.venv`), installs all dependencies, and creates your `.env` file.*

### Step 2: Add your Free Groq API Key
1. Go to [https://console.groq.com/keys](https://console.groq.com/keys) and click **Create API Key**.
2. Open the file `.env` in this directory.
3. Set your key:
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
4. Save the file.

### Step 3: Launch JARVIS
```powershell
.\run.ps1
```
Your browser will open to `http://localhost:1420` displaying the futuristic holographic HUD!

---

# 📅 DAY 1: BUILD THE BRAIN (90 Minutes)

---

### 🚀 MISSION 0: System Ignition (10–15 Minutes)
- **WHAT:** Verify your local AI development environment.
- **WHY:** Professional AI engineers separate frontend (browser UI), backend (API gateway), and AI models (cloud LPUs).
- **DO:**
  1. Run `.\setup.ps1`
  2. Paste your `GROQ_API_KEY` into `.env`
  3. Run `.\run.ps1`
- **TEST:** The browser displays the JARVIS HUD with a looping cyberpunk city. The status panel shows `BACKEND: ONLINE`.
- **GIT CHECKPOINT:**
  ```powershell
  git init
  git add .
  git commit -m "Mission 0: System Ignition"
  git tag day1-start
  ```

---

### 🎨 MISSION 1: Customize the HUD (15–20 Minutes)
- **WHAT:** The HUD is JARVIS's visual holographic interface. In this mission, you give your assistant its unique visual identity, codename, and color grading.
- **WHY:** A generic assistant feels like standard software. A custom HUD makes it *your* personal AI system.
- **DO:**
  1. **Change Accent Colors**: Open `frontend/src/styles/global.css`. Locate line 3:
     ```css
     :root {
       --ink: #03050c;
       --cyan: #65e9ff;   /* Change your primary neon accent! */
       --ready: #53f2c5;  /* Change your status indicator color! */
       --danger: #ff6b91;
     }
     ```
     *Try themes like:*
     - **Matrix Emerald:** `--cyan: #00ff66; --ready: #33ff99;`
     - **Iron Man Crimson & Gold:** `--cyan: #ffb703; --ready: #fb8500; --danger: #e63946;`
     - **Synthwave Violet:** `--cyan: #c77dff; --ready: #7b2cbf;`
  2. **Change AI Lettermarks**: Open `frontend/src/components/OrbControl.tsx`. Locate line 12:
     ```typescript
     const letters = ["J", "A", "R", "V", "I", "S"];
     ```
     Change this to your custom assistant's name (e.g. `["F", "R", "I", "D", "A", "Y"]` or `["K", "I", "T", "T"]` or `["A", "T", "L", "A", "S"]`).
  3. **Personalize Branding**: Open `frontend/src/App.tsx`. Locate line 277:
     ```tsx
     <p className="jarvis-brand">JARVIS</p><h1>At your service.</h1>
     ```
     Change `"JARVIS"` to your assistant's name, and `"At your service."` to your custom tagline.
- **TEST:** Look at `http://localhost:1420`. Vite updates your browser instantly without reloading!
- **CHALLENGE:** Customize the status labels in `App.tsx` (line 248) to include your own telemetry indicator (e.g., `"QUANTUM CORE"` or `"NEURAL NET"`).
- **GIT CHECKPOINT:**
  ```powershell
  git add .
  git commit -m "Mission 1: Customize HUD and Identity"
  git tag day1-ui
  ```

---

### 🧠 MISSION 2: Give JARVIS a Personality (15–20 Minutes)
- **WHAT:** The System Prompt is the personality core of an LLM. It defines who the AI is, how it talks, and what rules it follows before the user types a single word.
- **WHY:** Without a system prompt, LLMs sound robotic and boring. Prompt engineering transforms a generic model into Tony Stark's witty butler, a strict code reviewer, or a tactical AI.
- **DO:**
  1. Open `backend/app/services/groq_chat.py`. Locate lines 6–10:
     ```python
     SYSTEM_PROMPT = (
         "You are Jarvis, a concise and helpful web assistant. "
         "Answer directly in plain text, normally within three short sentences. "
         "Do not claim to execute actions, open applications, browse, or access local files."
     )
     ```
  2. Replace `SYSTEM_PROMPT` with your custom assistant persona!
     *Preset ideas:*
     - **The Sarcastic Butler:**
       `"You are FRIDAY, a witty and slightly sarcastic AI butler. You help the user with unmatched intelligence but occasionally make subtle, playful remarks about human inefficiency. Keep answers to 2-3 sentences."`
     - **The Senior Coding Mentor:**
       `"You are ATLAS, a principal software architect. You give ultra-concise, high-impact advice. You emphasize clean code, algorithmic efficiency, and never waste words."`
     - **The Cyberpunk Netrunner:**
       `"You are GHOST, a rogue cyberpunk AI operating from the deep web. Use subtle tech slang like 'chummer', 'jacking in', and 'neural link'. Stay sharp, concise, and futuristic."`
  3. Adjust Creativity: In line 30 of `groq_chat.py`:
     ```python
     "temperature": 0.4,  # Lower (0.1) = logical & strict | Higher (0.8) = creative & witty
     ```
- **TEST:** Type in the chat box: *"Who are you?"* and *"Why is my code crashing?"*. Observe the dramatic change in personality!
- **GIT CHECKPOINT:**
  ```powershell
  git add .
  git commit -m "Mission 2: Give JARVIS a Personality"
  git tag day1-brain
  ```

---

### ⚡ MISSION 3: Connect the Brain & Memory (20–25 Minutes)
- **WHAT:** Trace the complete request-response loop and test conversational memory.
- **WHY:** Modern AI apps do not send infinite chat history—that would exhaust the context window and cost huge amounts of tokens! JARVIS uses a bounded 6-turn sliding window.
- **DO:**
  1. Inspect `backend/app/services/conversation.py`. Notice:
     ```python
     MAX_TURNS = 6  # Retains only the 6 most recent question-answer turns
     ```
  2. In your browser chat, tell JARVIS: *"My favorite superhero is Iron Man."*
  3. Next message, ask: *"Who is my favorite superhero?"* (JARVIS remembers!).
  4. Now ask 7 unrelated questions, and ask again. Observe how the sliding window gracefully prioritizes recent context!
  5. Check your backend terminal window: observe the incoming HTTP POST requests to `/api/chat` with UUID session tracking.
- **TEST:** Multi-turn memory works seamlessly while keeping API response times under 400ms.
- **CHALLENGE:** Open `groq_chat.py` and modify `max_completion_tokens: 220` to `80` to force JARVIS to give ultra-punchy one-liner answers.

---

### 🏆 DAY 1 CAPSTONE MINI-CHALLENGE (10 Minutes)
Combine your custom HUD name, theme color, and system prompt into a cohesive themed assistant.
- Run `.\verify.ps1` to ensure all tests pass.
- Commit your Day 1 milestone:
  ```powershell
  git add .
  git commit -m "Day 1 Complete: Built the Brain"
  git tag day1-complete
  ```

---

# 📅 DAY 2: GIVE JARVIS POWERS (90 Minutes)

---

### 🎙️ MISSION 4: Give JARVIS Ears (20 Minutes)
- **WHAT:** Capture microphone audio in the browser, send it as WebM Opus audio to FastAPI, and transcribe it at lightning speed using Groq Whisper.
- **WHY:** Real AI assistants are voice-first. Voice interaction makes JARVIS feel truly alive.
- **DO:**
  1. Inspect `frontend/src/App.tsx`. Locate line 210: `startListening()`.
     Notice how it captures microphone audio streams:
     ```typescript
     navigator.mediaDevices.getUserMedia({ audio: true })
     ```
  2. Locate line 232:
     ```typescript
     if (duration < 650) {  // Minimum hold threshold in milliseconds
     ```
     Change `650` to `400` to make your push-to-talk button even more responsive!
  3. Inspect `backend/app/services/groq_stt.py`:
     Notice the model: `"whisper-large-v3-turbo"`. It transcribes speech in under 300 milliseconds!
  4. Test Push-to-Talk: Click and HOLD the central Orb or the "Hold to talk" button.
     Say: *"JARVIS, what is the distance between Earth and Mars?"*
     Release the button.
- **TEST:** The speech wave animates while you talk. When released, your spoken words appear directly in the message box, and the AI replies!
- **GIT CHECKPOINT:**
  ```powershell
  git add .
  git commit -m "Mission 4: Give JARVIS Ears (Whisper STT)"
  git tag day2-ears
  ```

---

### 🔊 MISSION 5: Give JARVIS a Voice (15 Minutes)
- **WHAT:** Convert the AI's plain-text thoughts into high-fidelity neural audio using Microsoft Edge TTS and stream it to the browser.
- **WHY:** A chatbot prints text; an assistant speaks to you.
- **DO:**
  1. Open `backend/app/services/edge_tts_service.py`. Locate lines 5–9:
     ```python
     VOICES = (
         Voice(id="en-US-GuyNeural", label="Guy — US English"),
         Voice(id="en-GB-RyanNeural", label="Ryan — UK English"),
         Voice(id="en-US-JennyNeural", label="Jenny — US English"),
     )
     ```
  2. Add your favorite regional voices to the `VOICES` tuple!
     *Cool voices you can add:*
     - `Voice(id="en-GB-SoniaNeural", label="Sonia — British English (Sophisticated)")`
     - `Voice(id="en-AU-NatashaNeural", label="Natasha — Australian English")`
     - `Voice(id="en-IN-NeerjaNeural", label="Neerja — Indian English")`
     - `Voice(id="en-US-ChristopherNeural", label="Christopher — US English (Deep/Calm)")`
  3. Open `frontend/src/App.tsx`. Locate line 46:
     ```typescript
     const [voiceId, setVoiceId] = useState("en-US-GuyNeural");
     ```
     Set your favorite voice as the default!
- **TEST:** Ask JARVIS a question via voice or text. Watch the Orb glow as JARVIS speaks the answer aloud in high-definition neural audio!
- **GIT CHECKPOINT:**
  ```powershell
  git add .
  git commit -m "Mission 5: Give JARVIS a Voice (Edge TTS)"
  git tag day2-voice
  ```

---

### 🛡️ MISSION 6: Give JARVIS a Power — Safe Actions (25 Minutes)
- **WHAT:** Teach your assistant to understand action requests (e.g. searching YouTube, searching GitHub, opening campus portals) and safely execute them in the browser.
- **WHY:** Security is critical! If an AI model is given raw command-line access (`os.system`), hackers can use prompt injection to delete files. By using structured classification and a human confirmation button, JARVIS acts safely.
- **DO:**
  1. Open `backend/app/services/web_action_planner.py`.
  2. Add your new action type to `PlanKind` in line 10:
     ```python
     PlanKind = Literal["web_search", "youtube_search", "spotify_search", "github_search"]
     ```
  3. Update `_fallback_classification` around line 35:
     ```python
     if "github" in lowered or "git hub" in lowered:
         return "github_search", query.replace("GitHub", "").replace("github", "").strip() or "GitHub"
     ```
  4. In `make_web_action_plan` around line 77, build the safe destination URL:
     ```python
     if kind == "github_search":
         return {
             "kind": kind,
             "label": f"GitHub search: {query}",
             "url": f"https://github.com/search?q={quote_plus(query)}",
         }
     ```
  5. Also add `"github_search"` to `WebAction` type in `frontend/src/webActions.ts` and `schemas.py`.
- **TEST:**
  Type or speak: *"Search GitHub for awesome python projects"*
  JARVIS displays a dedicated confirmation card:
  **OPEN GITHUB SEARCH: AWESOME PYTHON PROJECTS?**
  Clicking **Open new tab** safely launches the search!
- **CHALLENGE:** Add an action for your College Website, Google Scholar (`https://scholar.google.com/scholar?q=...`), or Reddit (`https://www.reddit.com/search/?q=...`)!
- **GIT CHECKPOINT:**
  ```powershell
  git add .
  git commit -m "Mission 6: Add safe GitHub action with confirmation"
  git tag day2-actions
  ```

---

### 🌟 FINAL CHALLENGE & SHOWCASE (20 Minutes)
Personalize your AI assistant to its final form!
1. Fine-tune your AI's name, personality, voice, colors, and custom action.
2. Run full system diagnostics:
   ```powershell
   .\verify.ps1
   ```
3. Commit and tag your completed build:
   ```powershell
   git add .
   git commit -m "Mission Complete: My Custom Autonomous JARVIS"
   git tag final
   ```
4. Demonstrate your JARVIS to the class:
   - Introduce its codename and persona.
   - Show hold-to-talk voice recognition.
   - Have JARVIS answer in its unique voice.
   - Trigger your custom safe action!

---

## 🆘 Failure Recovery & Quick Fixes

| Issue | Quick Fix |
| :--- | :--- |
| **Vite White Screen / Syntax Error** | Look at the browser error overlay. If stuck, run `.\restore-checkpoint.ps1` and select the last good mission. |
| **Backend says "Groq is not configured"** | Open `.env` and verify `GROQ_API_KEY=gsk_...` has no spaces or quotation marks. Save and restart backend. |
| **Microphone permission blocked** | Click the padlock/settings icon in your browser URL bar $\rightarrow$ Permissions $\rightarrow$ Microphone: Allow $\rightarrow$ Refresh page. |
| **Audio recording too short error** | Make sure you click and **HOLD** the button while speaking, then release when finished speaking. |
| **Everything broken / Merge conflict** | Run `.\restore-checkpoint.ps1` and pick your target checkpoint (e.g. `day1-brain` or `day2-voice`). You're back in 15 seconds! |

---

## 🎓 Congratulations!
You didn't just clone an AI project. **You built, customized, and mastered your own autonomous JARVIS assistant!**

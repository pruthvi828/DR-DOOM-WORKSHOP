# ⚡ MY CUSTOM JARVIS ASSISTANT

> **Student Project Dashboard**: Edit this section as you complete each mission to document your custom AI system!

---

### 📋 Assistant Information Sheet

- **Assistant Codename:** `[FILL IN: e.g. FRIDAY / ATLAS / GHOST]`
- **Creator / Student Name:** `[FILL IN: YOUR NAME]`
- **HUD Theme Palette:** `[FILL IN: e.g. Matrix Emerald / Synthwave Violet]`
- **AI Personality Persona:** `[FILL IN: e.g. Sarcastic Butler / Senior Coding Mentor]`
- **Selected Neural Voice:** `[FILL IN: e.g. Sonia UK English / Neerja Indian English]`
- **Custom Web Actions Built:** `[FILL IN: e.g. GitHub Search / College Portal]`

---

### 🏆 Mission Progress Tracker

- [x] **Mission 0: System Ignition & API Setup**
- [ ] **Mission 1: Holographic HUD & Visual Branding**
- [ ] **Mission 2: AI Personality Core & System Prompt**
- [ ] **Mission 3: Bounded Conversation Memory**
- [ ] **Mission 4: Speech-to-Text (Whisper STT)**
- [ ] **Mission 5: Text-to-Speech (Edge Neural TTS)**
- [ ] **Mission 6: Safe Autonomous Web Actions**

---

## 🛠️ Prerequisites & Fast Start

- Windows Laptop (Windows 10 or 11)
- Python 3.11+ installed
- Node.js 18+ installed
- Free Groq API Key ([console.groq.com](https://console.groq.com/))

### Step 1: Clone & Run Setup
```powershell
.\setup.ps1
```

### Step 2: Add your Free Groq API Key
Open `.env` and paste your key:
```env
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3: Launch Assistant
```powershell
.\run.ps1
```

---

# 🚀 MISSION 0: System Ignition

- **WHAT:** Verify your local AI development environment.
- **DO:**
  1. Run `.\setup.ps1`
  2. Paste your `GROQ_API_KEY` into `.env`
  3. Run `.\run.ps1`
- **TEST:** Your browser displays the basic chatbot interface. Send a message to confirm your backend is connected!

---

# 🎨 MISSION 1: Customize the Holographic HUD

- **WHAT:** Give your assistant its unique visual identity, codename, and color grading.
- **DO:**
  1. **Accent Colors**: Open `frontend/src/styles/global.css` (lines 10–15) and set your neon colors (`--cyan`, `--ready`).
  2. **Orb Letters**: Open `frontend/src/components/OrbControl.tsx` (line 14) and set `const letters = ["F","R","I","D","A","Y"];`.
  3. **Branding Header**: Open `frontend/src/App.tsx` (line 280) and set your codename header `<p className="jarvis-brand">FRIDAY</p>`.
  4. **Document Your Work**: Fill in the **Assistant Information Sheet** at the top of this `README.md` file and check off Mission 1!

- **TEST:** Save files and check `http://localhost:1420`.

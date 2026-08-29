# ⚡ JARVIS AI Assistant Workshop: Flight Manual

Welcome to the **JARVIS AI Assistant Workshop**! You are going to build and customize your own autonomous AI assistant.

```
    ┌───────────────────────────────────────────────────────────┐
    │                     WORKSHOP PHILOSOPHY                   │
    │  clone → run → understand → modify → integrate → test     │
    │                   ⚡ UNLOCK NEXT ABILITY ⚡                │
    └───────────────────────────────────────────────────────────┘
```

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

### Step 3: Launch Your Assistant
```powershell
.\run.ps1
```
Your browser will open to `http://localhost:1420` displaying the starter chatbot interface!

---

# 🚀 MISSION 0: System Ignition

- **WHAT:** Verify your local AI development environment.
- **WHY:** Professional AI software separates the frontend browser interface (React) from the secure backend API (FastAPI) and cloud AI models (Groq).
- **DO:**
  1. Run `.\setup.ps1`
  2. Paste your `GROQ_API_KEY` into `.env`
  3. Run `.\run.ps1`
- **TEST:** Your browser displays the basic chatbot interface. Send a message to confirm your backend is connected!

---

# 🎨 MISSION 1: Customize the Holographic HUD

- **WHAT:** The HUD is your AI assistant's visual interface. In this mission, you give your assistant its unique visual identity, codename, and color grading.
- **WHY:** A generic chatbot feels basic. A custom HUD makes it *your* personal AI system.
- **DO:**
  1. **Change Accent Colors**: Open `frontend/src/styles/global.css`. Locate lines 10–15:
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
     - **Cyber Amber:** `--cyan: #ffbe0b; --ready: #ffd166;`

  2. **Reprogram Orb Lettermarks**: Open `frontend/src/components/OrbControl.tsx`. Locate line 14:
     ```typescript
     const letters = ["F", "R", "I", "D", "A", "Y"];
     ```
     Add your custom assistant's lettermarks!

  3. **Personalize Branding**: Open `frontend/src/App.tsx`. Locate line 280:
     ```tsx
     <p className="jarvis-brand">FRIDAY</p><h1>Systems online.</h1>
     ```
     Change `"UNNAMED ASSISTANT"` to your custom codename, and `"System unconfigured."` to your custom tagline.

- **TEST:** Look at `http://localhost:1420`. The browser updates instantly via Vite Hot Reload!

---

## 🆘 Troubleshooting & Quick Fixes

| Issue | Quick Fix |
| :--- | :--- |
| **Vite White Screen / Syntax Error** | Check your browser console for error line numbers. |
| **Backend says "Groq is not configured"** | Open `.env` and verify `GROQ_API_KEY=gsk_...` has no quotes or extra spaces. Save and restart backend. |
| **Port 8765 or 1420 occupied** | Close extra PowerShell windows and re-run `.\run.ps1`. |

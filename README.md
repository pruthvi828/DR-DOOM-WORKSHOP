# ⚡ MY JARVIS ASSISTANT

### 📋 Student Dashboard
- **Assistant Codename:** `[YOUR ASSISTANT NAME]`
- **Student Name:** `[YOUR NAME]`
- **Theme Palette:** `[YOUR THEME]`

---

## 🚀 Mission 0: Quick Start

### 1. Run Setup
```powershell
.\setup.ps1
```

### 2. Add Groq API Key
Open `.env` and paste your key from [console.groq.com/keys](https://console.groq.com/keys):
```env
GROQ_API_KEY=gsk_your_key_here
```

### 3. Launch App
```powershell
.\run.ps1
```
Open `http://localhost:1420` in your browser!

---

## 📤 Push Progress to Your Own GitHub Repo

1. Create a new empty repository on **[github.com/new](https://github.com/new)** (e.g., `my-jarvis`).
2. Run these commands in PowerShell to save & push your work to your account:
```powershell
git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
git add .
git commit -m "Save my custom JARVIS assistant progress"
git push -u origin main
```

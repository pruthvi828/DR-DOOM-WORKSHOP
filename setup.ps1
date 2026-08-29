# ====================================================================
# JARVIS WORKSHOP // ONE-CLICK AUTOMATED SETUP
# ====================================================================
# This script automates environment setup (Node, Python, venv, packages).
# It does NOT automate your learning or coding challenges!
# ====================================================================

$ErrorActionPreference = "Stop"

function Write-Hud([string]$text, [string]$color = "Cyan") {
    Write-Host " [JARVIS] $text" -ForegroundColor $color
}

function Write-Banner {
    Clear-Host
    Write-Host " ╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host " ║                 JARVIS AI ASSISTANT WORKSHOP                    ║" -ForegroundColor Cyan
    Write-Host " ║              Autonomous System Ignition & Setup                ║" -ForegroundColor Cyan
    Write-Host " ╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

Write-Banner

# --------------------------------------------------------------------
# 1. VERIFY PYTHON
# --------------------------------------------------------------------
Write-Hud "Step 1/6: Checking Python environment..." "Yellow"

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host " [ERROR] Python was not found in your PATH!" -ForegroundColor Red
    Write-Host " Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host " Make sure to check the box: 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

$pyVersionRaw = & $pythonCmd --version 2>&1
Write-Hud "Found $pyVersionRaw" "Green"

# --------------------------------------------------------------------
# 2. VERIFY NODE.JS & NPM
# --------------------------------------------------------------------
Write-Hud "Step 2/6: Checking Node.js environment..." "Yellow"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host " [ERROR] Node.js was not found in your PATH!" -ForegroundColor Red
    Write-Host " Please install Node.js (LTS version) from https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

$nodeVersion = & node -v
$npmVersion = & npm -v
Write-Hud "Found Node.js $nodeVersion (npm v$npmVersion)" "Green"

# --------------------------------------------------------------------
# 3. SETUP PYTHON VIRTUAL ENVIRONMENT
# --------------------------------------------------------------------
Write-Hud "Step 3/6: Setting up Python virtual environment (backend/.venv)..." "Yellow"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"
$venvDir = Join-Path $backendDir ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Hud "Creating new virtual environment..." "DarkCyan"
    & $pythonCmd -m venv $venvDir
}

Write-Hud "Installing Python dependencies (FastAPI, Groq client, Edge-TTS, Pytest)..." "DarkCyan"
& $venvPython -m pip install --upgrade pip --quiet
& $venvPython -m pip install -r (Join-Path $backendDir "requirements.txt") pytest --quiet

Write-Hud "Backend virtual environment ready." "Green"

# --------------------------------------------------------------------
# 4. SETUP FRONTEND PACKAGES (NPM)
# --------------------------------------------------------------------
Write-Hud "Step 4/6: Installing frontend dependencies (React 19, TypeScript, Vite)..." "Yellow"

Push-Location $frontendDir
try {
    npm install --no-audit --no-fund --loglevel error
} finally {
    Pop-Location
}

Write-Hud "Frontend dependencies installed successfully." "Green"

# --------------------------------------------------------------------
# 5. CONFIGURE ENVIRONMENT (.env)
# --------------------------------------------------------------------
Write-Hud "Step 5/6: Configuring environment file (.env)..." "Yellow"

$rootEnv = Join-Path $scriptDir ".env"
$rootEnvExample = Join-Path $scriptDir ".env.example"
$backendEnv = Join-Path $backendDir ".env"

if (-not (Test-Path $rootEnv)) {
    if (Test-Path $rootEnvExample) {
        Copy-Item $rootEnvExample $rootEnv
        Write-Hud "Created .env from .env.example" "Green"
    }
}

if (-not (Test-Path $backendEnv)) {
    if (Test-Path (Join-Path $backendDir ".env.example")) {
        Copy-Item (Join-Path $backendDir ".env.example") $backendEnv
    }
}

$hasKey = $false
if (Test-Path $rootEnv) {
    $envContent = Get-Content $rootEnv -Raw
    if ($envContent -match 'GROQ_API_KEY=gsk_[a-zA-Z0-9_-]+') {
        $hasKey = $true
    }
}

# --------------------------------------------------------------------
# 6. VERIFY ASSETS & FINAL CHECK
# --------------------------------------------------------------------
Write-Hud "Step 6/6: Verifying assets..." "Yellow"

$assetsDir = Join-Path $scriptDir "assets"
if (-not (Test-Path $assetsDir)) {
    New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
}

Write-Host ""
Write-Host " ══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  SETUP COMPLETE! YOUR JARVIS WORKSPACE IS ARMED AND READY.       " -ForegroundColor Green
Write-Host " ══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

if (-not $hasKey) {
    Write-Host " [ACTION REQUIRED: ADD YOUR GROQ API KEY]" -ForegroundColor Magenta
    Write-Host " 1. Get your free Groq API key: https://console.groq.com/keys" -ForegroundColor White
    Write-Host " 2. Open the file: .env" -ForegroundColor White
    Write-Host " 3. Set your key: GROQ_API_KEY=gsk_your_key_here" -ForegroundColor Yellow
    Write-Host " 4. Save the file." -ForegroundColor White
    Write-Host ""
} else {
    Write-Host " [API KEY DETECTED] Groq key is already configured in .env!" -ForegroundColor Green
    Write-Host ""
}

Write-Host " To start JARVIS, run:" -ForegroundColor Cyan
Write-Host "   .\run.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host " To test your installation, run:" -ForegroundColor Cyan
Write-Host "   .\verify.ps1" -ForegroundColor Yellow
Write-Host ""

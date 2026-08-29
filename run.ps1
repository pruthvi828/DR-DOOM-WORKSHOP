# ====================================================================
# JARVIS WORKSHOP // DUAL LAUNCHER
# ====================================================================
# Starts the FastAPI backend (port 8765) and Vite frontend (port 1420),
# then opens your browser to the JARVIS HUD.
# ====================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"
$venvPython = Join-Path $backendDir ".venv\Scripts\python.exe"

# 1. Verify Setup was run
if (-not (Test-Path $venvPython)) {
    Write-Host ""
    Write-Host " [!] Virtual environment not found. Running setup.ps1 first..." -ForegroundColor Yellow
    & (Join-Path $scriptDir "setup.ps1")
}

# 2. Check for .env
$rootEnv = Join-Path $scriptDir ".env"
if (-not (Test-Path $rootEnv)) {
    Copy-Item (Join-Path $scriptDir ".env.example") $rootEnv
}

Write-Host ""
Write-Host " ╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host " ║                 IGNITING JARVIS ASSISTANT                      ║" -ForegroundColor Cyan
Write-Host " ╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host " [1/2] Starting FastAPI Backend on http://127.0.0.1:8765..." -ForegroundColor Green

# Launch backend in a dedicated visible window so students can observe API logs in real-time
$backendCmd = "Set-Location '$backendDir'; `$host.UI.RawUI.WindowTitle = 'JARVIS BACKEND [FastAPI :8765]'; & '$venvPython' -m uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

# Wait a brief moment for FastAPI to initialize
Start-Sleep -Seconds 2

Write-Host " [2/2] Starting Vite Frontend on http://localhost:1420..." -ForegroundColor Green

# Open browser to JARVIS HUD
Start-Process "http://localhost:1420"

# Run Vite dev server in the current console
Set-Location $frontendDir
npm run dev

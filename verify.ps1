# ====================================================================
# JARVIS WORKSHOP // SYSTEM VERIFICATION SUITE
# ====================================================================
# Runs backend pytest suite and frontend TypeScript compilation checks.
# ====================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"
$venvPython = Join-Path $backendDir ".venv\Scripts\python.exe"

Clear-Host
Write-Host " ╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host " ║              JARVIS WORKSHOP DIAGNOSTIC SUITE                  ║" -ForegroundColor Cyan
Write-Host " ╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$backendPass = $false
$frontendPass = $false

# 1. TEST BACKEND
Write-Host " [1/2] Running Backend Pytest Suite..." -ForegroundColor Yellow
if (Test-Path $venvPython) {
    Push-Location $backendDir
    try {
        & $venvPython -m pytest tests -q
        if ($LASTEXITCODE -eq 0) {
            $backendPass = $true
            Write-Host "  --> Backend tests passed cleanly!" -ForegroundColor Green
        } else {
            Write-Host "  --> Backend test failures detected." -ForegroundColor Red
        }
    } finally {
        Pop-Location
    }
} else {
    Write-Host "  --> Virtual environment not found. Run .\setup.ps1 first." -ForegroundColor Red
}

Write-Host ""

# 2. TEST FRONTEND
Write-Host " [2/2] Running Frontend Typecheck & Production Build..." -ForegroundColor Yellow
Push-Location $frontendDir
try {
    npm run build
    if ($LASTEXITCODE -eq 0) {
        $frontendPass = $true
        Write-Host "  --> Frontend compilation & build passed cleanly!" -ForegroundColor Green
    } else {
        Write-Host "  --> Frontend build errors detected." -ForegroundColor Red
    }
} finally {
    Pop-Location
}

Write-Host ""
Write-Host " ══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
if ($backendPass -and $frontendPass) {
    Write-Host "  ALL SYSTEMS OPERATIONAL: JARVIS IS READY FOR ACTION!            " -ForegroundColor Green
} else {
    Write-Host "  ISSUES DETECTED: Check error messages above to resolve.         " -ForegroundColor Yellow
}
Write-Host " ══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

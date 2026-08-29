# ====================================================================
# JARVIS WORKSHOP // CHECKPOINT RECOVERY ASSISTANT
# ====================================================================
# Use this script if you ever get stuck or break your code during a mission!
# It lets you restore known-good working checkpoints without restarting.
# ====================================================================

param(
    [ValidateSet("day1-start", "day1-ui", "day1-brain", "day2-voice", "day2-actions", "final")]
    [string]$Checkpoint
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Clear-Host
Write-Host " ╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host " ║           JARVIS WORKSHOP // CHECKPOINT RECOVERY               ║" -ForegroundColor Cyan
Write-Host " ╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

if (-not $Checkpoint) {
    Write-Host " Select a checkpoint to restore:" -ForegroundColor Yellow
    Write-Host " [1] day1-start   - Fresh starter project (Mission 0)" -ForegroundColor White
    Write-Host " [2] day1-ui      - Customized HUD & Identity (Mission 1)" -ForegroundColor White
    Write-Host " [3] day1-brain   - Personality & Groq Brain (Missions 2 & 3)" -ForegroundColor White
    Write-Host " [4] day2-voice   - Ears (STT) & Voice (TTS) (Missions 4 & 5)" -ForegroundColor White
    Write-Host " [5] day2-actions - Safe Web Actions & Intent Planner (Mission 6)" -ForegroundColor White
    Write-Host " [6] final        - Complete Reference Build" -ForegroundColor White
    Write-Host ""
    $choice = Read-Host " Enter choice (1-6)"

    switch ($choice) {
        "1" { $Checkpoint = "day1-start" }
        "2" { $Checkpoint = "day1-ui" }
        "3" { $Checkpoint = "day1-brain" }
        "4" { $Checkpoint = "day2-voice" }
        "5" { $Checkpoint = "day2-actions" }
        "6" { $Checkpoint = "final" }
        default {
            Write-Host "Invalid selection. Aborted." -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host " Restoring checkpoint: $Checkpoint..." -ForegroundColor Cyan

# Check if git tag exists
$hasGit = Test-Path (Join-Path $scriptDir ".git")
if ($hasGit) {
    $tagCheck = git tag -l $Checkpoint 2>$null
    if ($tagCheck) {
        git checkout $Checkpoint
        Write-Host " Restored via git tag: $Checkpoint" -ForegroundColor Green
        exit 0
    }
}

# Fallback to checkpoints directory
$checkpointDir = Join-Path $scriptDir "checkpoints\$Checkpoint"
if (Test-Path $checkpointDir) {
    Copy-Item -Path "$checkpointDir\*" -Destination $scriptDir -Recurse -Force
    Write-Host " Checkpoint '$Checkpoint' restored successfully from backup cache!" -ForegroundColor Green
} else {
    Write-Host " [!] Checkpoint files not found in cache. Checking reference build..." -ForegroundColor Yellow
    $referenceDir = Join-Path (Split-Path -Parent $scriptDir) "JARVIS-FINAL"
    if (Test-Path $referenceDir) {
        Copy-Item -Path "$referenceDir\backend\app\services\*" -Destination (Join-Path $scriptDir "backend\app\services") -Recurse -Force
        Copy-Item -Path "$referenceDir\frontend\src\*" -Destination (Join-Path $scriptDir "frontend\src") -Recurse -Force
        Write-Host " Restored working reference code from JARVIS-FINAL!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host " Run .\verify.ps1 to confirm system health, then .\run.ps1 to resume." -ForegroundColor Yellow
Write-Host ""

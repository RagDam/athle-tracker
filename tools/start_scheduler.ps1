# Athle Tracker - Script de démarrage du Scheduler
# Usage: .\start_scheduler.ps1

Write-Host "⏰ Démarrage du Scheduler Athle Tracker..." -ForegroundColor Cyan
Write-Host ""

# Vérifier si on est dans le bon dossier
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Vérifier si le venv existe
if (-Not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "❌ Environnement virtuel non trouvé!" -ForegroundColor Red
    Write-Host "Exécutez d'abord: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activer le venv
Write-Host "📦 Activation de l'environnement virtuel..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Définir PYTHONPATH
$env:PYTHONPATH = $scriptPath
Write-Host "✅ PYTHONPATH configuré: $scriptPath" -ForegroundColor Green
Write-Host ""

# Lancer le scheduler
Write-Host "🤖 Lancement du Scheduler..." -ForegroundColor Cyan
Write-Host "⏰ Fenêtre de scraping: 01:45 - 03:15 (Europe/Paris)" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Le scheduler scrape automatiquement chaque jour" -ForegroundColor Gray
Write-Host "💡 Pour arrêter: CTRL + C" -ForegroundColor Gray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

python src\infrastructure\scheduler\run_scheduler.py

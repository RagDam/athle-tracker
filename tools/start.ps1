# Athle Tracker - Script de démarrage
# Usage: .\start.ps1

Write-Host "🏃 Démarrage d'Athle Tracker..." -ForegroundColor Cyan
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

# Vérifier si la base de données existe
if (-Not (Test-Path "athle_tracker.db")) {
    Write-Host "⚠️  Base de données non trouvée. Initialisation..." -ForegroundColor Yellow
    python -m src.infrastructure.database.init_db
    Write-Host ""
}

# Définir PYTHONPATH
$env:PYTHONPATH = $scriptPath
Write-Host "✅ PYTHONPATH configuré: $scriptPath" -ForegroundColor Green
Write-Host ""

# Lancer Streamlit
Write-Host "🚀 Lancement de Streamlit..." -ForegroundColor Cyan
Write-Host "📍 URL: http://localhost:8501" -ForegroundColor Yellow
Write-Host "🔐 Credentials: admin@example.com / admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Pour arrêter: CTRL + C" -ForegroundColor Gray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

streamlit run src\presentation\streamlit\app.py

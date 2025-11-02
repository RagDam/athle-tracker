# Athle Tracker - Script de démarrage Next.js + FastAPI
# Usage: .\tools\start.ps1

Write-Host "🏃 Démarrage d'Athle Tracker..." -ForegroundColor Cyan
Write-Host ""

# Aller à la racine du projet
$rootPath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $rootPath

Write-Host "📍 Dossier racine: $rootPath" -ForegroundColor Gray
Write-Host ""

# Vérifier si le venv existe
if (-Not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "❌ Environnement virtuel non trouvé!" -ForegroundColor Red
    Write-Host "Exécutez d'abord: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Vérifier si node_modules existe
if (-Not (Test-Path "frontend\node_modules")) {
    Write-Host "❌ Node modules non trouvés!" -ForegroundColor Red
    Write-Host "Exécutez d'abord: cd frontend && npm install" -ForegroundColor Yellow
    exit 1
}

# Vérifier si la base de données existe
if (-Not (Test-Path "athle_tracker.db")) {
    Write-Host "⚠️  Base de données non trouvée. Initialisation..." -ForegroundColor Yellow
    & "venv\Scripts\python.exe" -m src.infrastructure.database.init_db
    Write-Host ""
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🚀 Lancement des serveurs..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📦 Backend FastAPI:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "🎨 Frontend Next.js: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔐 Credentials: admin@example.com / admin123" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Pour arrêter: CTRL + C dans chaque terminal" -ForegroundColor Gray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# Lancer le backend FastAPI dans un nouveau terminal
Write-Host "▶️  Lancement du backend FastAPI..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootPath'; venv\Scripts\activate; `$env:PYTHONPATH='$rootPath'; python src/api/main.py"

# Attendre 3 secondes
Start-Sleep -Seconds 3

# Lancer le frontend Next.js dans un nouveau terminal
Write-Host "▶️  Lancement du frontend Next.js..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootPath\frontend'; npm run dev"

Write-Host ""
Write-Host "✅ Serveurs lancés avec succès!" -ForegroundColor Green
Write-Host "🌐 Ouvrez http://localhost:3000 dans votre navigateur" -ForegroundColor Cyan
Write-Host ""

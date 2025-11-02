# Script pour pousser le projet vers GitHub
Write-Host "======================================"
Write-Host "PUSH VERS GITHUB - ATHLE TRACKER"
Write-Host "======================================"
Write-Host ""

# 1. Supprimer ancien .git
Write-Host "[1/7] Suppression ancien repo git..."
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
Write-Host "OK - Ancien .git supprime"
Write-Host ""

# 2. Initialiser nouveau repo
Write-Host "[2/7] Initialisation nouveau repo git..."
git init
Write-Host "OK - Repo initialise"
Write-Host ""

# 3. Ajouter tous les fichiers
Write-Host "[3/7] Ajout de tous les fichiers..."
git add .
Write-Host "OK - Fichiers ajoutes"
Write-Host ""

# 4. Premier commit
Write-Host "[4/7] Creation du commit initial..."
git commit -m "feat: initial commit - Next.js 14 + FastAPI"
Write-Host "OK - Commit cree"
Write-Host ""

# 5. Ajouter remote
Write-Host "[5/7] Ajout du remote GitHub..."
git remote add origin https://github.com/RagDam/athle-tracker.git
Write-Host "OK - Remote ajoute"
Write-Host ""

# 6. Renommer branche
Write-Host "[6/7] Renommage de la branche en main..."
git branch -M main
Write-Host "OK - Branche renommee"
Write-Host ""

# 7. Push vers GitHub
Write-Host "[7/7] Push vers GitHub..."
git push -u origin main

Write-Host ""
Write-Host "======================================"
Write-Host "PUSH TERMINE AVEC SUCCES !"
Write-Host "======================================"
Write-Host ""
Write-Host "Votre projet est maintenant sur :"
Write-Host "https://github.com/RagDam/athle-tracker"
Write-Host ""

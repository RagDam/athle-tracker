# Démarrage des serveurs Athle Tracker

## Méthode 1 : Script automatique (recommandé)

Double-cliquez sur le fichier `start_servers.bat` dans l'explorateur Windows.

Cela va :
1. Arrêter tous les processus Python et Node existants
2. Démarrer le backend FastAPI sur http://localhost:8000
3. Démarrer le frontend Next.js sur http://localhost:3000

## Méthode 2 : Démarrage manuel

### 1. Arrêter les processus existants

Ouvrez un PowerShell ou CMD et exécutez :

```cmd
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### 2. Démarrer le backend FastAPI

Ouvrez un terminal dans le dossier du projet et exécutez :

```cmd
venv\Scripts\python.exe -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Le backend sera accessible sur http://localhost:8000

### 3. Démarrer le frontend Next.js

Ouvrez un AUTRE terminal dans le dossier `frontend` et exécutez :

```cmd
cd frontend
npm run dev -- -p 3000
```

Le frontend sera accessible sur http://localhost:3000

## URLs importantes

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Login** : http://localhost:3000/login

## Identifiants de test

### Admin
- Email : admin@test.com
- Mot de passe : admin123

### Utilisateur standard
- Email : user@test.com
- Mot de passe : user123

## Problèmes courants

### "Port 3000 is already in use"

Si Next.js dit que le port 3000 est occupé, c'est qu'un ancien serveur tourne encore.
Exécutez : `taskkill /F /IM node.exe` puis relancez le frontend.

### "Port 8000 is already in use"

Si FastAPI dit que le port 8000 est occupé, c'est qu'un ancien serveur tourne encore.
Exécutez : `taskkill /F /IM python.exe` puis relancez le backend.

### "Internal Server Error" sur la page de login

Vérifiez que :
1. Le backend FastAPI est bien démarré et répond sur http://localhost:8000/api/health
2. Le frontend est bien sur le port 3000 (pas 3001, 3002, etc.)
3. Il n'y a qu'un seul serveur de chaque type qui tourne

## Test des endpoints API

Pour tester tous les endpoints de l'API, exécutez :

```cmd
venv\Scripts\python.exe scripts\test_api_endpoints.py
```

Cela va tester l'authentification, les classements, les alertes, etc.

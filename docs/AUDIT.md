# 📋 AUDIT COMPLET DU PROJET ATHLE TRACKER

Date : 2025-11-02
Objectif : Nettoyer, factoriser et vérifier l'architecture après migration Next.js

---

## 🗂️ RÉPERTOIRES À SUPPRIMER

### 1. Streamlit (OBSOLÈTE - Migration Next.js effectuée)
- `src/presentation/streamlit/` - **SUPPRIMER** - Ancien UI Streamlit
- `src/presentation/streamlit/components/` - **SUPPRIMER**
- `src/presentation/streamlit/styles/` - **SUPPRIMER**
- `src/presentation/streamlit/views/` - **SUPPRIMER**
- `.streamlit/` - **SUPPRIMER** - Configuration Streamlit
- `src/presentation/` - **SUPPRIMER** (vide après suppression Streamlit)

### 2. Migrations (Non utilisées selon user)
- `migrations/` - **SUPPRIMER** - Migrations Alembic non nécessaires

### 3. Répertoires vides ou inutilisés
- `docs/` - **VÉRIFIER** si contient des docs utiles, sinon supprimer
- `logs/` - **GARDER** (pour les logs futurs du scraper)
- `tests/fixtures/` - **GARDER** (pour tests futurs)
- `tests/integration/` - **GARDER** (pour tests futurs)
- `tests/unit/` - **GARDER** (pour tests futurs)

---

## 📄 FICHIERS À SUPPRIMER

### Fichiers de test/debug
- `test_jwt.py` - **SUPPRIMER** - Script de test temporaire
- `decode_jwt.py` - **SUPPRIMER** - Script de debug temporaire
- `check_epreuves.py` - **SUPPRIMER** - Script de debug temporaire
- `test_scraper_debug.py` - **SUPPRIMER** - Script de debug
- `debug_response.html` - **SUPPRIMER** - Fichier de debug
- `.streamlit_session.json` - **SUPPRIMER** - Session Streamlit
- `nul` - **SUPPRIMER** - Fichier vide/erreur

### Fichiers de configuration obsolètes
- `.pre-commit-config.yaml` - **VÉRIFIER** si utilisé
- `pyproject.toml` - **VÉRIFIER** contenu vs requirements.txt
- `pytest.ini` - **GARDER** (pour tests futurs)

---

## 📂 RÉPERTOIRES À GARDER

### Backend (src/)
```
src/
├── api/                    ✅ FastAPI routes et dépendances
│   ├── routers/           ✅ Endpoints REST (auth, rankings, alerts, etc.)
│   ├── dependencies.py    ✅ JWT, DB session, auth
│   ├── main.py           ✅ App FastAPI principale
│   └── schemas.py        ✅ Pydantic schemas
├── config/               ✅ Configuration (settings.py)
├── core/                 ✅ Business logic (Clean Architecture)
│   ├── entities/        ✅ Entités métier
│   ├── interfaces/      ✅ Interfaces des repositories
│   └── use_cases/       ✅ Cas d'usage métier
├── infrastructure/       ✅ Implémentations techniques
│   ├── auth/            ✅ Authentification
│   ├── database/        ✅ SQLAlchemy models + repositories
│   ├── scheduler/       ✅ Scraping automatique
│   └── scraper/         ✅ Scraper athle.fr
└── utils/               ✅ Utilitaires
```

### Frontend (frontend/)
```
frontend/
├── app/                  ✅ Next.js App Router
│   ├── (auth)/login/    ✅ Page de connexion
│   ├── (dashboard)/     ✅ Pages protégées
│   │   ├── admin/      ✅ Administration
│   │   ├── alerts/     ✅ Alertes
│   │   ├── dashboard/  ✅ Dashboard
│   │   ├── favorites/  ✅ Favoris
│   │   └── rankings/   ✅ Classements
│   ├── layout.tsx      ✅ Layout racine
│   └── globals.css     ✅ Styles globaux
├── components/          ✅ Composants React
│   ├── layout/         ✅ Header, Sidebar, MainLayout
│   └── ui/             ✅ shadcn/ui components
├── lib/                ✅ Utilitaires
│   └── api/client.ts   ✅ Client API Axios
├── types/              ✅ Types TypeScript
└── public/             ✅ Assets statiques
```

### Scripts
```
scripts/
├── init_admin.py         ✅ Création users admin/test
└── test_api_endpoints.py ✅ Test endpoints API
```

### Configuration
```
.
├── .env.example          ✅ Variables d'environnement exemple
├── .gitignore           ✅ Git ignore
├── requirements.txt     ✅ Dépendances Python
├── requirements-dev.txt ✅ Dépendances dev Python
├── package.json         ✅ Dépendances Node.js (frontend/)
├── start_servers.bat    ✅ Script démarrage serveurs
├── restart_servers.py   ✅ Script redémarrage Python
└── start.ps1            ✅ Script PowerShell démarrage
```

### Documentation
```
.
├── README.md            ✅ Documentation principale
├── CLAUDE.md           ✅ Best practices développement
├── DEMARRAGE.md        ✅ Guide démarrage serveurs
├── PROJECT_SUMMARY.md  ✅ Résumé projet
├── QUICKSTART.md       ✅ Guide rapide
└── LICENSE             ✅ Licence
```

---

## 🔍 FICHIERS À VÉRIFIER/REFACTORISER

### 1. Duplication de code
- **repositories** : Vérifier si `SQLAlchemyUserRepository`, `SQLAlchemyRankingRepository`, etc. ont du code dupliqué
- **routers** : Vérifier duplication dans auth, rankings, alerts

### 2. Code mort (unused functions)
- `src/core/use_cases/` - Vérifier si tous les use cases sont utilisés
- `src/infrastructure/auth/` - Vérifier si utilisé ou si tout est dans dependencies.py

### 3. Configuration
- `.env` - **CRÉER** si manquant (copier de .env.example)
- Vérifier cohérence entre `pyproject.toml` et `requirements.txt`

---

## 📊 RÉSUMÉ

### À SUPPRIMER (19 items)
1. ❌ `src/presentation/` (tout le dossier Streamlit)
2. ❌ `.streamlit/`
3. ❌ `migrations/`
4. ❌ `test_jwt.py`
5. ❌ `decode_jwt.py`
6. ❌ `check_epreuves.py`
7. ❌ `test_scraper_debug.py`
8. ❌ `debug_response.html`
9. ❌ `.streamlit_session.json`
10. ❌ `nul`

### À VÉRIFIER (5 items)
1. ⚠️ `docs/` - Contenu ?
2. ⚠️ `.pre-commit-config.yaml` - Utilisé ?
3. ⚠️ `pyproject.toml` vs `requirements.txt`
4. ⚠️ `src/infrastructure/auth/` - Utilisé ?
5. ⚠️ Code dupliqué dans repositories

### À GARDER (Tout le reste)
- ✅ Backend FastAPI (src/api/, src/core/, src/infrastructure/)
- ✅ Frontend Next.js (frontend/)
- ✅ Scripts utiles (scripts/)
- ✅ Configuration (requirements, .env.example, etc.)
- ✅ Documentation (.md files)
- ✅ Tests (tests/)

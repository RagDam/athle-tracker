# 🏃 Athle Tracker

Application web moderne de suivi des classements athlétiques FFA pour le javelot.

**Stack** : FastAPI + Next.js 14 + SQLite + shadcn/ui

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Node.js 18+
- Git

### Installation

```bash
# 1. Cloner le repo
git clone <repo-url>
cd athle-tracker

# 2. Installer les dépendances Python
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Installer les dépendances Node.js
cd frontend
npm install
cd ..

# 4. Créer le fichier .env
cp .env.example .env

# 5. Initialiser la base de données et créer les users
python scripts/init_admin.py
```

### Démarrage des serveurs

**Option 1 : Script automatique (recommandé)**
```bash
# Windows
tools\start_servers.bat

# OU PowerShell
.\tools\start.ps1
```

**Option 2 : Manuel**
```bash
# Terminal 1 - Backend FastAPI
venv\Scripts\python.exe -m uvicorn src.api.main:app --reload --port 8000

# Terminal 2 - Frontend Next.js
cd frontend && npm run dev -- -p 3000
```

### Accès

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

### Identifiants de test

**Admin** :
- Email : admin@test.com
- Mot de passe : admin123

**User** :
- Email : user@test.com
- Mot de passe : user123

---

## 📚 Documentation

Toute la documentation est dans le dossier [`docs/`](docs/)

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Guide de démarrage rapide
- **[DEMARRAGE.md](docs/DEMARRAGE.md)** - Guide de démarrage détaillé
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Architecture complète du projet
- **[CLAUDE.md](docs/CLAUDE.md)** - Best practices de développement
- **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Résumé du projet
- **[AUDIT.md](docs/AUDIT.md)** - Rapport d'audit du code

---

## 🏗️ Structure du projet

```
athle-tracker/
├── frontend/          # Next.js 14 + shadcn/ui
├── src/              # Backend FastAPI + Business Logic
│   ├── api/         # Endpoints REST
│   ├── core/        # Business logic (Clean Architecture)
│   └── infrastructure/  # DB, scraper, scheduler
├── scripts/          # Scripts utilitaires (init DB, tests)
├── tools/           # Scripts de démarrage
├── docs/            # Documentation complète
└── tests/           # Tests pytest
```

Voir [ARCHITECTURE.md](docs/ARCHITECTURE.md) pour les détails complets.

---

## ✨ Fonctionnalités

- ✅ **Scraping automatique** des classements athle.fr
- ✅ **Authentification JWT** avec rôles (admin/user)
- ✅ **Dashboard moderne** avec Next.js 14 + shadcn/ui
- ✅ **Classements en temps réel** avec historique
- ✅ **Alertes personnalisées** pour changements de position
- ✅ **Gestion des favoris** pour suivre des athlètes
- ✅ **Panel admin** pour gérer épreuves et utilisateurs
- ✅ **Clean Architecture** (Core/Infrastructure/API)

---

## 🧪 Tests

```bash
# Tester tous les endpoints API
python scripts/test_api_endpoints.py

# Tests unitaires (à venir)
pytest tests/unit

# Tests d'intégration (à venir)
pytest tests/integration
```

---

## 🛠️ Développement

### Standards de code

Voir [CLAUDE.md](docs/CLAUDE.md) pour les best practices complètes.

**Résumé** :
- ✅ Type hints obligatoires
- ✅ Docstrings pour fonctions publiques
- ✅ Fonctions < 50 lignes
- ✅ DRY (Don't Repeat Yourself)
- ✅ Clean Architecture stricte

### Formatage

```bash
# Python
black src/ --line-length 100
ruff check src/

# TypeScript
cd frontend && npm run lint
```

---

## 📝 Licence

MIT License - Voir [LICENSE](docs/LICENSE)

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'feat: Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📞 Support

Pour toute question, ouvrir une issue sur GitHub.

---

**Dernière mise à jour** : 2025-11-02
**Version** : 2.0.0 (Migration Next.js)

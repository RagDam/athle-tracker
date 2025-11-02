# 🏗️ ARCHITECTURE DU PROJET ATHLE TRACKER

Date : 2025-11-02
Stack : FastAPI + Next.js 14 + SQLite + SQLAlchemy

---

## 📂 STRUCTURE COMPLÈTE

```
athle-tracker/
│
├── 📁 frontend/                    # Frontend Next.js 14
│   ├── app/                       # Next.js App Router
│   │   ├── (auth)/               # Routes non authentifiées
│   │   │   └── login/            # Page de connexion
│   │   ├── (dashboard)/          # Routes authentifiées
│   │   │   ├── admin/            # Administration (admin only)
│   │   │   ├── alerts/           # Centre de notifications
│   │   │   ├── dashboard/        # Dashboard principal
│   │   │   ├── favorites/        # Gestion des favoris
│   │   │   └── rankings/         # Classements en temps réel
│   │   ├── layout.tsx            # Layout racine (font, metadata)
│   │   └── globals.css           # Styles globaux Tailwind
│   │
│   ├── components/               # Composants React réutilisables
│   │   ├── layout/              # Composants de mise en page
│   │   │   ├── header.tsx       # Header avec navigation
│   │   │   ├── sidebar.tsx      # Sidebar conditionnelle
│   │   │   └── main-layout.tsx  # Layout principal
│   │   └── ui/                  # shadcn/ui components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── table.tsx
│   │       ├── badge.tsx
│   │       ├── tabs.tsx
│   │       └── ... (15+ composants)
│   │
│   ├── lib/                     # Utilitaires et helpers
│   │   ├── api/                 # Client API
│   │   │   └── client.ts        # Axios client + endpoints
│   │   └── utils.ts             # Utilitaires divers
│   │
│   ├── types/                   # Types TypeScript
│   │   └── index.ts            # Interfaces User, Ranking, etc.
│   │
│   ├── public/                  # Assets statiques
│   │
│   ├── .eslintrc.json          # Configuration ESLint
│   ├── next.config.mjs         # Configuration Next.js
│   ├── package.json            # Dépendances Node.js
│   ├── postcss.config.mjs      # Configuration PostCSS
│   ├── tailwind.config.ts      # Configuration Tailwind CSS
│   └── tsconfig.json           # Configuration TypeScript
│
├── 📁 src/                         # Backend FastAPI + Business Logic
│   ├── api/                       # Couche API (FastAPI)
│   │   ├── routers/              # Endpoints REST
│   │   │   ├── __init__.py      # Router registry
│   │   │   ├── auth.py          # POST /api/auth/login
│   │   │   ├── rankings.py      # GET /api/rankings/*
│   │   │   ├── alerts.py        # GET /api/alerts/*
│   │   │   ├── epreuves.py      # CRUD /api/epreuves/*
│   │   │   ├── users.py         # CRUD /api/users/* (admin)
│   │   │   └── scraping.py      # POST /api/scraping/run (admin)
│   │   ├── dependencies.py       # JWT, DB session, auth helpers
│   │   ├── main.py              # FastAPI app + CORS + routers
│   │   └── schemas.py           # Pydantic request/response models
│   │
│   ├── config/                   # Configuration
│   │   └── settings.py          # Pydantic Settings (DB, JWT, etc.)
│   │
│   ├── core/                     # Business Logic (Clean Architecture)
│   │   ├── entities/            # Entités métier (DTOs)
│   │   │   └── ranking_dto.py   # Data Transfer Objects
│   │   ├── interfaces/          # Interfaces des repositories
│   │   │   └── repositories.py  # ABC pour repositories
│   │   └── use_cases/           # Cas d'usage métier
│   │       └── scrape_rankings.py # Use case scraping
│   │
│   ├── infrastructure/           # Implémentations techniques
│   │   ├── database/            # SQLAlchemy ORM
│   │   │   ├── models.py        # User, Ranking, Athlete, etc.
│   │   │   ├── repositories.py  # Implémentations repositories
│   │   │   └── session.py       # Session factory
│   │   ├── scheduler/           # Scraping automatique
│   │   │   └── scraping_scheduler.py # APScheduler
│   │   └── scraper/             # Scraper athle.fr
│   │       └── athle_scraper.py # Scraper avec retry logic
│   │
│   └── utils/                    # Utilitaires
│       └── logger.py            # Configuration logging
│
├── 📁 scripts/                     # Scripts utilitaires
│   ├── init_admin.py             # Créer users admin/test
│   └── test_api_endpoints.py    # Tester tous les endpoints
│
├── 📁 tests/                       # Tests (pytest)
│   ├── fixtures/                # Fixtures réutilisables
│   ├── integration/             # Tests d'intégration
│   └── unit/                    # Tests unitaires
│
├── 📁 logs/                        # Logs du scraper
│
├── 📄 Configuration
│   ├── .env.example             # Variables d'environnement exemple
│   ├── .gitignore              # Git ignore
│   ├── requirements.txt        # Dépendances Python production
│   ├── requirements-dev.txt    # Dépendances Python dev
│   ├── pyproject.toml          # Config Black/Ruff
│   └── pytest.ini              # Config pytest
│
├── 📄 Scripts de démarrage
│   ├── start_servers.bat       # Windows batch
│   ├── restart_servers.py      # Python script
│   └── start.ps1              # PowerShell script
│
├── 📄 Documentation
│   ├── README.md              # Documentation principale
│   ├── CLAUDE.md             # Best practices développement
│   ├── DEMARRAGE.md          # Guide démarrage
│   ├── PROJECT_SUMMARY.md    # Résumé projet
│   ├── QUICKSTART.md         # Guide rapide
│   ├── ARCHITECTURE.md       # Ce fichier
│   ├── AUDIT.md              # Rapport d'audit
│   └── LICENSE               # Licence MIT
│
└── 📄 Données
    └── athle_tracker.db       # Base SQLite (gitignored)
```

---

## 🏛️ ARCHITECTURE EN COUCHES (Clean Architecture)

### 1️⃣ Core (Domain Layer)
**Responsabilité** : Business logic pure, indépendante de toute implémentation

```python
src/core/
├── entities/       # DTOs (Data Transfer Objects)
├── interfaces/     # Abstract Base Classes pour repositories
└── use_cases/      # Cas d'usage métier (ex: ScrapeRankingsUseCase)
```

**Règles d'or** :
- ❌ Ne dépend JAMAIS de Infrastructure ou Presentation
- ✅ Contient uniquement la logique métier
- ✅ Utilise des interfaces (ABC) pour les dépendances

### 2️⃣ Infrastructure Layer
**Responsabilité** : Implémentations techniques (DB, scraper, scheduler)

```python
src/infrastructure/
├── database/       # SQLAlchemy models + repositories
├── scheduler/      # APScheduler pour scraping auto
└── scraper/        # Scraper athle.fr avec retry logic
```

**Règles d'or** :
- ✅ Implémente les interfaces définies dans Core
- ✅ Accède aux ressources externes (DB, API, fichiers)
- ❌ Ne contient PAS de logique métier

### 3️⃣ API Layer (Presentation)
**Responsabilité** : Exposition REST API avec FastAPI

```python
src/api/
├── routers/        # Endpoints REST
├── dependencies.py # JWT, DB session, auth
├── main.py        # FastAPI app
└── schemas.py     # Pydantic request/response
```

**Règles d'or** :
- ✅ Utilise Infrastructure via Dependency Injection
- ✅ Valide les entrées avec Pydantic
- ✅ Gère l'authentification JWT
- ❌ Ne contient PAS de logique métier

### 4️⃣ Frontend (Next.js)
**Responsabilité** : Interface utilisateur avec React

```typescript
frontend/
├── app/            # Pages Next.js App Router
├── components/     # Composants React réutilisables
├── lib/api/        # Client API Axios
└── types/          # Types TypeScript
```

**Règles d'or** :
- ✅ Communique avec le backend via API REST
- ✅ Gère l'état local avec React hooks
- ✅ Authentification JWT dans localStorage
- ❌ Aucune logique métier (uniquement UI)

---

## 🔄 FLUX DE DONNÉES

### Exemple : Afficher les classements

```
1. User clique sur "Classements" dans le frontend
   ↓
2. Frontend (rankings/page.tsx)
   → Appelle rankingsApi.getAll() via Axios
   ↓
3. Backend (src/api/routers/rankings.py)
   → Endpoint GET /api/rankings/all
   → Vérifie JWT (get_current_user)
   ↓
4. Repository (src/infrastructure/database/repositories.py)
   → SQLAlchemyRankingRepository.get_latest_by_epreuve()
   → Query SQLAlchemy sur la DB
   ↓
5. Backend
   → Mappe Ranking model → RankingResponse schema
   → Retourne JSON
   ↓
6. Frontend
   → Reçoit les données
   → Affiche dans un Table component
```

---

## 🔐 SÉCURITÉ

### Authentification
- **JWT** avec expiration (défini dans settings)
- **Secret key** stockée dans .env (JAMAIS en dur)
- **Password hashing** avec bcrypt

### Autorisation
- **Role-based access control** (admin/user)
- **Protected routes** avec get_current_user dependency
- **Admin-only endpoints** avec get_current_admin_user

### Frontend
- **Token JWT** stocké dans localStorage
- **Authorization header** : `Bearer <token>`
- **Redirection** vers /login si non authentifié

---

## 📊 BASE DE DONNÉES

### Tables principales
```sql
users           → Utilisateurs (admin/user)
epreuves        → Épreuves athlétiques (ex: Javelot)
athletes        → Athlètes (nom, athlete_id)
rankings        → Classements (snapshots quotidiens)
alerts          → Notifications de changement de rang
favorites       → Athlètes favoris par user
scrape_logs     → Logs du scraper
```

### Relations
```
User 1---N Favorite N---1 Athlete
User 1---N Alert N---1 Athlete
Epreuve 1---N Ranking N---1 Athlete
```

---

## 🚀 DÉPLOIEMENT

### Development
```bash
# Backend
venv\Scripts\python.exe -m uvicorn src.api.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev -- -p 3000
```

### Production (à venir)
- **Backend** : Gunicorn + Uvicorn workers
- **Frontend** : npm run build + serveur Node.js
- **DB** : Migration vers PostgreSQL recommandée
- **Reverse proxy** : Nginx
- **HTTPS** : Certbot (Let's Encrypt)

---

## ✅ CONFORMITÉ CLEAN ARCHITECTURE

### ✅ Ce qui est BIEN
- Core ne dépend de rien
- Infrastructure implémente les interfaces de Core
- API utilise Infrastructure via DI
- Séparation claire des responsabilités

### ⚠️ Points d'amélioration futurs
- Ajouter des tests unitaires pour les use cases
- Implémenter plus de use cases (actuellement 1 seul)
- Ajouter validation métier dans Core (actuellement dans API)

---

**Dernière mise à jour : 2025-11-02**
**Version : 2.0.0** (Migration Next.js)

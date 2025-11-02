# 🏃 Athle Tracker

Système de tracking d'évolution de classements athle.fr avec interface web moderne, système d'alertes intelligentes et gestion de favoris.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Tests](#-tests)
- [Développement](#-développement)
- [Contribution](#-contribution)

---

## 🎯 Vue d'ensemble

**Athle Tracker** est un système complet permettant de suivre quotidiennement l'évolution des classements d'athlètes sur [athle.fr](https://www.athle.fr). Il offre une interface web moderne, un système d'alertes automatiques pour les changements significatifs, et une gestion des athlètes favoris.

### Cas d'usage

- 🏅 **Entraîneurs** : Suivre la progression de leurs athlètes
- 👨‍👩‍👧‍👦 **Parents** : Suivre les performances de leurs enfants
- 📊 **Analystes** : Étudier les tendances des performances
- 📰 **Journalistes** : Suivre les actualités sportives

---

## ✨ Fonctionnalités

### Core Features

- ✅ **Scraping Automatisé**
  - Scraping quotidien automatique (fenêtre aléatoire 01:45-03:15)
  - Scraping manuel via interface admin
  - Anti-détection (User-Agents rotatifs, délais variables)
  - Retry automatique avec backoff exponentiel
  - Logs complets de toutes les opérations

- ✅ **Interface Web Moderne**
  - Authentification sécurisée (rôles User/Admin)
  - Dashboard avec KPIs et statistiques
  - Graphiques interactifs (Plotly)
  - Podiums animés (🥇🥈🥉)
  - Design moderne avec gradients et glassmorphism
  - Responsive mobile

- ✅ **Système d'Alertes Intelligentes**
  - **Top 3** (podium) → Alerte critique
  - **Top 10** → Alerte importante
  - **Top 20** → Alerte info
  - **Favoris** (toute variation) → Alerte info
  - Notifications dans l'interface
  - Compteur d'alertes non lues

- ✅ **Gestion des Favoris**
  - Ajout/retrait d'athlètes favoris
  - Suivi personnalisé des performances
  - Alertes dédiées

- ✅ **Panel Admin Complet**
  - CRUD des épreuves
  - CRUD des utilisateurs
  - Configuration du scraping
  - Scraping manuel
  - Consultation des logs

---

## 🏗️ Architecture

### Clean Architecture

Le projet suit les principes de **Clean Architecture** avec séparation claire des couches :

```
src/
├── core/                      # Logique métier (Business Logic)
│   ├── entities/             # Entités du domaine
│   ├── use_cases/            # Cas d'usage
│   └── interfaces/           # Interfaces (Repository Pattern)
├── infrastructure/           # Implémentations techniques
│   ├── database/             # SQLAlchemy ORM + Repositories
│   ├── scraper/              # Scraping athle.fr
│   ├── scheduler/            # APScheduler
│   └── auth/                 # Authentification
├── presentation/             # Couche présentation
│   └── streamlit/            # Interface Streamlit
│       ├── app.py            # Point d'entrée
│       ├── pages/            # Pages de l'application
│       ├── components/       # Composants réutilisables
│       └── styles/           # CSS personnalisé
├── config/                   # Configuration
└── utils/                    # Utilitaires
```

### Stack Technique

| Composant | Technologie | Version |
|-----------|------------|---------|
| **Framework** | Streamlit | 1.31.0 |
| **Database** | SQLite + SQLAlchemy | 2.0.25 |
| **Scraping** | httpx + BeautifulSoup4 | 0.26.0 |
| **Scheduler** | APScheduler | 3.10.4 |
| **Auth** | passlib[bcrypt] | 1.7.4 |
| **Charts** | Plotly | 5.18.0 |
| **Testing** | pytest + pytest-cov | 8.0.0 |
| **Linting** | ruff + black + mypy | Latest |

---

## 📦 Installation

### Prérequis

- Python 3.11+
- pip
- Git

### Étapes

1. **Cloner le repository**

```bash
git clone https://github.com/RagDam/athle-tracker.git
cd athle-tracker
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Configurer l'environnement**

```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

5. **Initialiser la base de données**

```bash
python -m src.infrastructure.database.init_db
```

Cela va créer :
- ✅ Les tables de la base de données
- ✅ L'épreuve **Javelot** (code 670)
- ✅ L'utilisateur **admin@example.com** / **admin123**

---

## ⚙️ Configuration

Toute la configuration se fait via le fichier `.env` :

```bash
# Database
DATABASE_URL=sqlite:///./athle_tracker.db

# Scraping
SCRAPING_MIN_DELAY=2.0
SCRAPING_MAX_DELAY=3.0
SCRAPING_MAX_RETRIES=3

# Scheduler
SCHEDULER_ENABLED=True
SCHEDULER_START_HOUR=1
SCHEDULER_START_MINUTE=45
SCHEDULER_END_HOUR=3
SCHEDULER_END_MINUTE=15
TIMEZONE=Europe/Paris

# Security
SECRET_KEY=your-secret-key-change-this
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

⚠️ **Important** : Changez `SECRET_KEY` et les identifiants admin en production !

---

## 🚀 Utilisation

### Lancer l'application web

```bash
streamlit run src/presentation/streamlit/app.py
```

L'interface sera accessible sur **http://localhost:8501**

### Lancer le scheduler (scraping automatique)

Dans un terminal séparé :

```bash
python src/infrastructure/scheduler/run_scheduler.py
```

Le scheduler :
- 🕐 Scrape quotidiennement entre 01:45 et 03:15
- 🎲 Choisit une heure aléatoire dans cette fenêtre
- 🔄 Scrape automatiquement toutes les épreuves actives
- 📊 Génère les alertes automatiquement

### Scraping manuel

Vous pouvez également déclencher un scraping manuel depuis l'interface admin :

1. Se connecter en tant qu'admin
2. Aller dans **🤖 Scraping**
3. Sélectionner l'épreuve et le genre
4. Cliquer sur **🚀 Lancer le scraping**

---

## 🧪 Tests

### Installer les dépendances de développement

```bash
pip install -r requirements-dev.txt
```

### Lancer les tests

```bash
# Tous les tests avec coverage
pytest --cov=src --cov-report=html

# Tests unitaires uniquement
pytest tests/unit/

# Tests d'intégration uniquement
pytest tests/integration/

# Rapport de coverage en HTML
open htmlcov/index.html
```

### Linting et Formatting

```bash
# Formatting avec Black
black src/

# Linting avec Ruff
ruff check src/

# Type checking avec Mypy
mypy src/

# Tout en une fois
black src/ && ruff check src/ && mypy src/
```

### Pre-commit Hooks

```bash
# Installer les hooks
pre-commit install

# Lancer manuellement
pre-commit run --all-files
```

---

## 👨‍💻 Développement

### Structure du Code

- **Use Cases** : Logique métier pure (pas de dépendances externes)
- **Repositories** : Interfaces définies dans `core/interfaces/`
- **Implementations** : Implémentations concrètes dans `infrastructure/`
- **Dependency Injection** : Session SQLAlchemy injectée dans les repositories

### Ajouter une nouvelle épreuve

1. Via l'interface admin :
   - Admin > Épreuves > Ajouter
   - Nom : "Disque"
   - Code : 671 (code athle.fr)

2. Le scraping automatique inclura cette épreuve

### Ajouter un nouvel utilisateur

1. Via l'interface admin :
   - Admin > Utilisateurs > Ajouter
   - Email, mot de passe, rôle

### Modèle de données

7 tables principales :

| Table | Description |
|-------|-------------|
| `users` | Utilisateurs (email, password_hash, role) |
| `epreuves` | Épreuves (nom, code, actif) |
| `athletes` | Athlètes (athlete_id, name) |
| `rankings` | Classements (snapshot_date, rank, performance) |
| `favorites` | Favoris utilisateurs |
| `alerts` | Alertes générées |
| `scrape_logs` | Logs des scrapings |

---

## 📚 Documentation Supplémentaire

- **[CLAUDE.md](./CLAUDE.md)** : Best practices pour développer avec Claude Code
- **[API Documentation](./docs/api.md)** : Documentation de l'API interne (à venir)
- **[Architecture Decision Records](./docs/adr/)** : Décisions d'architecture (à venir)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Créer une **branche feature** (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

### Guidelines

- ✅ Suivre les conventions de code (Black, Ruff)
- ✅ Ajouter des tests pour les nouvelles features
- ✅ Maintenir la coverage >80%
- ✅ Documenter les fonctions publiques
- ✅ Utiliser les type hints

---

## 📝 Changelog

### v1.0.0 (2025-11-02)

- 🎉 Version initiale
- ✅ Scraping Javelot Cadets 2026
- ✅ Interface Streamlit moderne
- ✅ Système d'alertes Top 3/10/20
- ✅ Authentification User/Admin
- ✅ Scheduler automatique

---

## 📄 License

Ce projet est sous licence MIT. Voir [LICENSE](./LICENSE) pour plus de détails.

---

## 👤 Auteur

**RagDam**
- GitHub: [@RagDam](https://github.com/RagDam)

---

## 🙏 Remerciements

- [athle.fr](https://www.athle.fr) pour les données
- [Streamlit](https://streamlit.io/) pour le framework
- [FastAPI](https://fastapi.tiangolo.com/) pour l'inspiration architecturale

---

## 📞 Support

Pour toute question ou problème :

1. 🐛 [Ouvrir une issue](https://github.com/RagDam/athle-tracker/issues)
2. 💬 [Discussions](https://github.com/RagDam/athle-tracker/discussions)
3. 📧 Email : *(à définir)*

---

**Made with ❤️ and ☕ by RagDam**

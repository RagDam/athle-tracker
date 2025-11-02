# 🚀 Quick Start Guide - Athle Tracker

Guide de démarrage rapide en 5 minutes.

---

## 📋 Prérequis

- ✅ Python 3.11+ installé
- ✅ Git installé
- ✅ Terminal / Command Prompt

---

## ⚡ Installation Express

### 1. Cloner et naviguer

```bash
cd e:\ONEDRIVE\1 - Personnel\Sites Web\athle-tracker
```

### 2. Activer l'environnement virtuel

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Initialiser la base de données

```bash
python -m src.infrastructure.database.init_db
```

**Résultat attendu :**
```
✅ Database initialized successfully
✅ Created admin user: admin@example.com
✅ Created Javelot event (code 670)
```

### 5. Lancer l'application

```bash
streamlit run src/presentation/streamlit/app.py
```

**L'app s'ouvrira automatiquement sur http://localhost:8501**

---

## 🔐 Première Connexion

**Credentials par défaut :**
- Email: `admin@example.com`
- Mot de passe: `admin123`

⚠️ **IMPORTANT** : Changez ces identifiants après la première connexion !

---

## 🎯 Premiers Pas

### 1. Dashboard
- Vue d'ensemble des classements
- KPIs et statistiques
- Podiums animés

### 2. Lancer un Scraping Manuel

1. Aller dans **🤖 Scraping** (menu admin)
2. Sélectionner **Javelot (Code 670)**
3. Choisir le genre (M ou F)
4. Cliquer sur **🚀 Lancer le scraping**

⏱️ Le scraping prend environ 10-15 secondes.

### 3. Consulter les Classements

1. Aller dans **📋 Classements**
2. Sélectionner l'épreuve et le genre
3. Voir tous les athlètes classés

### 4. Voir les Alertes

1. Aller dans **🔔 Alertes**
2. Consulter les alertes générées automatiquement
3. Marquer comme lu

---

## 🤖 Scraping Automatique (Optionnel)

Pour activer le scraping quotidien automatique :

**Dans un terminal séparé :**

```bash
python src/infrastructure/scheduler/run_scheduler.py
```

Le scheduler :
- ✅ Scrape quotidiennement entre 01:45 et 03:15
- ✅ Génère automatiquement les alertes
- ✅ Logs toutes les opérations

**Pour arrêter :** `CTRL + C`

---

## 🧪 Tester l'Installation

### Lancer les tests

```bash
# Installer les dépendances de dev
pip install -r requirements-dev.txt

# Lancer les tests
pytest --cov=src --cov-report=term-missing

# Résultat attendu : >80% coverage
```

### Vérifier le code

```bash
# Formatting
black src/

# Linting
ruff check src/

# Type checking
mypy src/
```

---

## 📁 Structure Rapide

```
athle-tracker/
├── src/
│   ├── core/               # Business logic
│   ├── infrastructure/     # Technical implementations
│   │   ├── database/       # SQLAlchemy + Repositories
│   │   ├── scraper/        # Web scraping
│   │   ├── scheduler/      # APScheduler
│   │   └── auth/           # Authentication
│   └── presentation/       # Streamlit UI
│       └── streamlit/
│           ├── app.py      # Entry point
│           ├── pages/      # Pages
│           └── styles/     # CSS
├── tests/                  # Unit + Integration tests
├── .env                    # Configuration
└── athle_tracker.db        # SQLite database (auto-créé)
```

---

## 🆘 Problèmes Courants

### Erreur : "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur : "Database not initialized"
```bash
python -m src.infrastructure.database.init_db
```

### Port 8501 déjà utilisé
```bash
streamlit run src/presentation/streamlit/app.py --server.port 8502
```

### Le CSS ne se charge pas
- Vérifier que le fichier existe : `src/presentation/streamlit/styles/custom.css`
- Relancer Streamlit

---

## 📚 Documentation Complète

- **[README.md](./README.md)** : Documentation complète
- **[CLAUDE.md](./CLAUDE.md)** : Best practices de développement

---

## 🎉 Vous êtes prêt !

L'application est maintenant fonctionnelle. Vous pouvez :

1. ✅ Scraper des classements
2. ✅ Consulter les résultats
3. ✅ Recevoir des alertes
4. ✅ Gérer les utilisateurs
5. ✅ Ajouter d'autres épreuves

---

## 🚀 Prochaines Étapes

### Ajouter une nouvelle épreuve

1. Admin > 🏅 Épreuves
2. Cliquer sur "➕ Ajouter une nouvelle épreuve"
3. Nom : "Disque", Code : **671** (code athle.fr)
4. Le scraping automatique l'inclura

### Créer un nouvel utilisateur

1. Admin > 👥 Utilisateurs
2. Ajouter un utilisateur avec rôle "user" ou "admin"

### Changer le mot de passe admin

1. Admin > 👥 Utilisateurs
2. Sélectionner admin@example.com
3. Changer le mot de passe

---

**Bon tracking ! 🏃‍♂️**

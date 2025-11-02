# 🤖 CLAUDE.md - Best Practices de Développement

Ce document définit les **standards de développement** et **best practices** pour le projet Athle Tracker. Il est destiné à être utilisé par Claude Code et les développeurs humains.

---

## 📋 Table des Matières

1. [Architecture & Design Patterns](#-architecture--design-patterns)
2. [Standards de Code](#-standards-de-code)
3. [Base de Données](#-base-de-données)
4. [Tests](#-tests)
5. [Sécurité](#-sécurité)
6. [Performance](#-performance)
7. [Documentation](#-documentation)
8. [Git Workflow](#-git-workflow)
9. [Intelligence de Migration](#-intelligence-de-migration)

---

## 🏗️ Architecture & Design Patterns

### Clean Architecture

Le projet suit strictement la **Clean Architecture** :

```
core/           ← Business Logic (ne dépend de rien)
↑
infrastructure/ ← Implémentations techniques
↑
presentation/   ← UI (Streamlit)
```

**Règles d'or :**

1. ✅ **Core ne dépend jamais de Infrastructure ou Presentation**
2. ✅ **Infrastructure implémente les interfaces définies dans Core**
3. ✅ **Presentation utilise Infrastructure via Dependency Injection**
4. ❌ **Jamais d'import direct de SQLAlchemy dans Core**
5. ❌ **Jamais d'import de Streamlit en dehors de Presentation**

### Repository Pattern

Toutes les opérations de données passent par des **repositories** :

```python
# ✅ BON : Interface dans core/interfaces/
class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

# ✅ BON : Implémentation dans infrastructure/
class SQLAlchemyUserRepository(UserRepository):
    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

# ❌ MAUVAIS : Accès direct à la DB dans Use Case
user = session.query(User).filter(User.email == email).first()
```

### Use Cases Pattern

Chaque **action métier** = 1 Use Case :

```python
# ✅ BON : Use Case dédié
class ScrapeRankingsUseCase:
    def __init__(self, session: Session) -> None:
        self.ranking_repo = SQLAlchemyRankingRepository(session)
        self.alert_repo = SQLAlchemyAlertRepository(session)

    async def execute(self, epreuve_code: int, sexe: str) -> dict:
        # Logique métier ici
        pass

# ❌ MAUVAIS : Logique métier dans le controller
def scrape_button_clicked():
    # 50 lignes de logique...
```

---

## 📝 Standards de Code

### Type Hints OBLIGATOIRES

```python
# ✅ BON
def get_rankings(epreuve_code: int, sexe: str) -> List[RankingDTO]:
    pass

# ❌ MAUVAIS
def get_rankings(epreuve_code, sexe):
    pass
```

### Docstrings pour Fonctions Publiques

```python
# ✅ BON
def scrape_rankings(epreuve_code: int) -> List[Dict]:
    """
    Scrape rankings from athle.fr.

    Args:
        epreuve_code: Competition code (e.g., 670 for javelin)

    Returns:
        List of ranking dictionaries

    Raises:
        ScrapingError: If scraping fails after retries
    """
    pass
```

### Fonctions Courtes (<50 lignes)

```python
# ✅ BON : Fonction courte et focalisée
def parse_performance(performance_str: str) -> tuple[str, float]:
    """Parse performance string to clean value and numeric."""
    clean = re.sub(r"\s*\([^)]*\)", "", performance_str).strip()
    match = re.match(r"(\d+)m(\d+)", clean)
    if match:
        meters = int(match.group(1))
        centimeters = int(match.group(2))
        return clean, meters + (centimeters / 100.0)
    return clean, 0.0

# ❌ MAUVAIS : Fonction trop longue (>100 lignes)
def scrape_and_process_everything():
    # 150 lignes...
```

### DRY (Don't Repeat Yourself)

```python
# ✅ BON : Réutilisation
def format_datetime(dt: datetime) -> str:
    return dt.strftime("%d/%m/%Y %H:%M")

# Usage
st.write(format_datetime(ranking.created_at))
st.write(format_datetime(alert.created_at))

# ❌ MAUVAIS : Duplication
st.write(ranking.created_at.strftime("%d/%m/%Y %H:%M"))
st.write(alert.created_at.strftime("%d/%m/%Y %H:%M"))
```

### Error Handling Robuste

```python
# ✅ BON : Try/except avec logging
try:
    result = await scraper.scrape_rankings(code, sexe)
except ScrapingError as e:
    logger.error(f"Scraping failed: {e}")
    return {"success": False, "error": str(e)}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# ❌ MAUVAIS : Silence les erreurs
try:
    result = scraper.scrape_rankings(code, sexe)
except:
    pass
```

---

## 🗄️ Base de Données

### Migrations

Toute modification du schéma = **migration Alembic** :

```bash
# Générer une migration
alembic revision --autogenerate -m "Add column X to table Y"

# Appliquer
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Indexes

Toujours créer des **indexes** pour :
- Foreign keys
- Colonnes utilisées dans WHERE
- Colonnes utilisées dans ORDER BY

```python
# ✅ BON : Indexes définis
__table_args__ = (
    Index("idx_ranking_date_epreuve_sexe", "snapshot_date", "epreuve_code", "sexe"),
)

# ❌ MAUVAIS : Pas d'index sur colonnes fréquentes
```

### Transactions

Utiliser **context managers** :

```python
# ✅ BON
with get_db_session() as session:
    user_repo = SQLAlchemyUserRepository(session)
    user = user_repo.create(user_data)
    # Auto-commit si succès, rollback si erreur

# ❌ MAUVAIS : Session manuelle non fermée
session = SessionLocal()
user = session.query(User).first()
# Oubli de session.close()
```

---

## 🧪 Tests

### Coverage >80% OBLIGATOIRE

```bash
pytest --cov=src --cov-report=html --cov-fail-under=80
```

### Tests Unitaires (Use Cases)

```python
# tests/unit/test_scrape_rankings.py
@pytest.mark.unit
def test_scrape_rankings_success(mock_session):
    """Test successful scraping."""
    use_case = ScrapeRankingsUseCase(mock_session)
    result = await use_case.execute(670, "M")

    assert result["success"] is True
    assert result["rankings_count"] > 0
```

### Tests d'Intégration (Scraper)

```python
# tests/integration/test_athle_scraper.py
@pytest.mark.integration
@pytest.mark.slow
async def test_scrape_real_data():
    """Test scraping real athle.fr data."""
    scraper = AthleScraper()
    rankings = await scraper.scrape_rankings(670, "M")

    assert len(rankings) > 0
    assert rankings[0]["rank"] == 1
```

### Fixtures Réutilisables

```python
# tests/fixtures/database.py
@pytest.fixture
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
```

---

## 🔒 Sécurité

### Passwords

```python
# ✅ BON : Toujours hasher
password_hash = bcrypt.hash(plain_password)

# ❌ MAUVAIS : Stocker en clair
user.password = plain_password
```

### SQL Injection

```python
# ✅ BON : Utiliser l'ORM
user = session.query(User).filter(User.email == email).first()

# ❌ MAUVAIS : SQL brut
session.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### Secrets

```python
# ✅ BON : Variables d'environnement
SECRET_KEY = os.getenv("SECRET_KEY")

# ❌ MAUVAIS : Hardcodé
SECRET_KEY = "super-secret-123"
```

---

## ⚡ Performance

### Bulk Operations

```python
# ✅ BON : Bulk insert
rankings = [Ranking(**data) for data in rankings_data]
session.bulk_save_objects(rankings)

# ❌ MAUVAIS : Boucle
for data in rankings_data:
    ranking = Ranking(**data)
    session.add(ranking)
    session.commit()  # Commit à chaque itération !
```

### N+1 Queries

```python
# ✅ BON : Eager loading
rankings = session.query(Ranking).options(
    joinedload(Ranking.athlete),
    joinedload(Ranking.epreuve)
).all()

# ❌ MAUVAIS : N+1
rankings = session.query(Ranking).all()
for r in rankings:
    print(r.athlete.name)  # Query pour chaque athlete !
```

### Caching

```python
# ✅ BON : Cache les requêtes lourdes
@st.cache_data(ttl=3600)
def get_rankings(epreuve_code: int, sexe: str) -> List[Dict]:
    # Calcul coûteux
    return rankings
```

---

## 📚 Documentation

### README.md

- Vue d'ensemble du projet
- Installation
- Configuration
- Utilisation

### CLAUDE.md (ce fichier)

- Best practices
- Standards de développement
- Conventions

### Docstrings

```python
# ✅ BON : Docstring complète
def scrape_rankings(
    epreuve_code: int,
    sexe: str,
    annee: int = 2026,
) -> List[Dict[str, Any]]:
    """
    Scrape rankings from athle.fr with retry logic.

    Args:
        epreuve_code: Competition code (e.g., 670 for Javelin)
        sexe: Gender (M or F)
        annee: Year (default 2026)

    Returns:
        List of ranking dictionaries with keys:
        - rank (int)
        - athlete_id (str)
        - name (str)
        - performance (str)
        - club (str)

    Raises:
        ScrapingError: If scraping fails after all retries

    Example:
        >>> rankings = await scraper.scrape_rankings(670, "M")
        >>> print(rankings[0])
        {'rank': 1, 'name': 'John Doe', ...}
    """
```

---

## 🔀 Git Workflow

### Branches

- `main` : Production-ready
- `develop` : Development
- `feature/nom-feature` : Nouvelles features
- `fix/nom-bug` : Bug fixes

### Commits

Format : `type(scope): message`

```bash
# ✅ BON
git commit -m "feat(scraper): add retry with exponential backoff"
git commit -m "fix(auth): prevent SQL injection in login"
git commit -m "docs(readme): update installation instructions"

# ❌ MAUVAIS
git commit -m "update"
git commit -m "fix bug"
```

Types :
- `feat` : Nouvelle feature
- `fix` : Bug fix
- `docs` : Documentation
- `refactor` : Refactoring
- `test` : Tests
- `chore` : Maintenance

---

## 🚀 Intelligence de Migration

### Triggers CRITIQUES (Proposer migration AVANT implémentation)

Si le user demande :
- 📱 Application mobile
- 🌐 API publique externe
- 👥 >100 users concurrent
- 🏢 SaaS multi-tenant

**Action :**
1. ⚠️ **STOP** : Ne pas implémenter
2. 💡 Proposer migration vers **FastAPI + React**
3. 📊 Estimer effort (10-12 jours)
4. ✅ Attendre validation user

### Triggers RECOMMANDÉS (Signaler APRÈS implémentation)

Si le projet atteint :
- 🏅 >4 épreuves actives
- 🎨 UI très customisée
- ⚡ Temps réel / WebSockets nécessaire
- 🐌 Performance dégradée (>3s page load)

**Action :**
1. ✅ Implémenter quand même
2. 💡 Mentionner dans le commit/PR
3. 📝 Documenter la limitation

---

## 🎯 Checklist Avant Commit

Avant chaque commit, vérifier :

- [ ] ✅ Code formaté avec Black
- [ ] ✅ Pas d'erreurs Ruff
- [ ] ✅ Pas d'erreurs Mypy
- [ ] ✅ Tests passent (pytest)
- [ ] ✅ Coverage >80%
- [ ] ✅ Docstrings à jour
- [ ] ✅ Type hints présents
- [ ] ✅ Logs appropriés
- [ ] ✅ Pas de secrets hardcodés
- [ ] ✅ README à jour si nécessaire

---

## 📞 Questions ?

Si doute sur :
- Architecture → Relire Clean Architecture
- Standards → Relire ce fichier
- Tests → Voir tests existants
- Sécurité → En parler AVANT d'implémenter

---

**Dernière mise à jour : 2025-11-02**
**Version : 1.0.0**

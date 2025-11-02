"""Pytest configuration and shared fixtures."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext

from src.infrastructure.database.models import Base, User, Epreuve, Athlete, Ranking

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="function")
def test_engine():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create test database session."""
    SessionLocal = sessionmaker(bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_admin_user(test_session: Session) -> User:
    """Create test admin user."""
    user = User(
        email="admin@test.com",
        password_hash=pwd_context.hash("testpassword123"),
        role="admin",
        created_at=datetime.now(),
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def test_regular_user(test_session: Session) -> User:
    """Create test regular user."""
    user = User(
        email="user@test.com",
        password_hash=pwd_context.hash("testpassword123"),
        role="user",
        created_at=datetime.now(),
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def test_epreuve(test_session: Session) -> Epreuve:
    """Create test epreuve (Javelot)."""
    epreuve = Epreuve(
        nom="Javelot",
        code=670,
        actif=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    test_session.add(epreuve)
    test_session.commit()
    test_session.refresh(epreuve)
    return epreuve


@pytest.fixture
def test_athlete(test_session: Session) -> Athlete:
    """Create test athlete."""
    athlete = Athlete(
        athlete_id="test_athlete_1",
        name="Test Athlete",
        first_seen_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    test_session.add(athlete)
    test_session.commit()
    test_session.refresh(athlete)
    return athlete


@pytest.fixture
def test_ranking(test_session: Session, test_epreuve: Epreuve, test_athlete: Athlete) -> Ranking:
    """Create test ranking."""
    ranking = Ranking(
        snapshot_date=datetime.now(),
        epreuve_code=test_epreuve.code,
        sexe="M",
        rank=1,
        athlete_id=test_athlete.athlete_id,
        performance="58m14",
        performance_numeric=58.14,
        club="Test Club",
        ligue="I-F",
        departement="093",
        created_at=datetime.now(),
    )
    test_session.add(ranking)
    test_session.commit()
    test_session.refresh(ranking)
    return ranking


@pytest.fixture
def sample_scrape_data():
    """Sample scraped data for testing."""
    return [
        {
            "rank": 1,
            "athlete_id": "navaud_roger_nathan",
            "name": "NAVAUD-ROGER Nathan",
            "performance": "58m14",
            "performance_numeric": 58.14,
            "club": "Ca Montreuil 93",
            "ligue": "I-F",
            "departement": "093",
            "infos": "CAM/09",
            "date": datetime(2025, 9, 28),
            "lieu": "Aulnay sous bois",
        },
        {
            "rank": 2,
            "athlete_id": "sence_robin",
            "name": "SENCE Robin",
            "performance": "49m29",
            "performance_numeric": 49.29,
            "club": "Artois Athletisme*",
            "ligue": "H-F",
            "departement": "062",
            "infos": "CAM/09",
            "date": datetime(2025, 10, 5),
            "lieu": "Bruay la buissiere",
        },
        {
            "rank": 3,
            "athlete_id": "klein_timeo",
            "name": "KLEIN Timeo",
            "performance": "49m10",
            "performance_numeric": 49.10,
            "club": "Fac Andrezieux",
            "ligue": "ARA",
            "departement": "042",
            "infos": "CAM/09",
            "date": datetime(2025, 9, 28),
            "lieu": "Grenoble",
        },
    ]

"""Unit tests for Repositories."""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from src.infrastructure.database.repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyEpreuveRepository,
    SQLAlchemyAthleteRepository,
    SQLAlchemyRankingRepository,
)
from src.infrastructure.database.models import User, Epreuve, Athlete, Ranking


@pytest.mark.unit
class TestUserRepository:
    """Test cases for SQLAlchemyUserRepository."""

    def test_get_by_email(self, test_session: Session, test_regular_user: User) -> None:
        """Test get user by email."""
        repo = SQLAlchemyUserRepository(test_session)

        user = repo.get_by_email(test_regular_user.email)

        assert user is not None
        assert user.email == test_regular_user.email

    def test_get_by_id(self, test_session: Session, test_regular_user: User) -> None:
        """Test get user by ID."""
        repo = SQLAlchemyUserRepository(test_session)

        user = repo.get_by_id(test_regular_user.id)

        assert user is not None
        assert user.id == test_regular_user.id

    def test_create(self, test_session: Session) -> None:
        """Test creating a user."""
        repo = SQLAlchemyUserRepository(test_session)

        user_data = {
            "email": "new@test.com",
            "password_hash": "hashed",
            "role": "user",
            "actif": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        user = repo.create(user_data)

        assert user.id is not None
        assert user.email == "new@test.com"

    def test_update(self, test_session: Session, test_regular_user: User) -> None:
        """Test updating a user."""
        repo = SQLAlchemyUserRepository(test_session)

        updated_user = repo.update(test_regular_user.id, {"role": "admin"})

        assert updated_user is not None
        assert updated_user.role == "admin"

    def test_delete(self, test_session: Session, test_regular_user: User) -> None:
        """Test deleting a user."""
        repo = SQLAlchemyUserRepository(test_session)

        result = repo.delete(test_regular_user.id)

        assert result is True

        # Verify deletion
        user = repo.get_by_id(test_regular_user.id)
        assert user is None

    def test_list_all(
        self, test_session: Session, test_regular_user: User, test_admin_user: User
    ) -> None:
        """Test listing all users."""
        repo = SQLAlchemyUserRepository(test_session)

        users = repo.list_all()

        assert len(users) >= 2
        assert any(u.email == test_regular_user.email for u in users)
        assert any(u.email == test_admin_user.email for u in users)


@pytest.mark.unit
class TestEpreuveRepository:
    """Test cases for SQLAlchemyEpreuveRepository."""

    def test_get_by_code(self, test_session: Session, test_epreuve: Epreuve) -> None:
        """Test get epreuve by code."""
        repo = SQLAlchemyEpreuveRepository(test_session)

        epreuve = repo.get_by_code(test_epreuve.code)

        assert epreuve is not None
        assert epreuve.code == test_epreuve.code

    def test_list_active(self, test_session: Session, test_epreuve: Epreuve) -> None:
        """Test listing active epreuves."""
        repo = SQLAlchemyEpreuveRepository(test_session)

        active_epreuves = repo.list_active()

        assert len(active_epreuves) >= 1
        assert any(e.code == test_epreuve.code for e in active_epreuves)

    def test_create(self, test_session: Session) -> None:
        """Test creating an epreuve."""
        repo = SQLAlchemyEpreuveRepository(test_session)

        epreuve_data = {
            "nom": "Disque",
            "code": 671,
            "actif": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        epreuve = repo.create(epreuve_data)

        assert epreuve.id is not None
        assert epreuve.nom == "Disque"


@pytest.mark.unit
class TestAthleteRepository:
    """Test cases for SQLAlchemyAthleteRepository."""

    def test_get_by_athlete_id(
        self, test_session: Session, test_athlete: Athlete
    ) -> None:
        """Test get athlete by athlete_id."""
        repo = SQLAlchemyAthleteRepository(test_session)

        athlete = repo.get_by_athlete_id(test_athlete.athlete_id)

        assert athlete is not None
        assert athlete.athlete_id == test_athlete.athlete_id

    def test_create(self, test_session: Session) -> None:
        """Test creating an athlete."""
        repo = SQLAlchemyAthleteRepository(test_session)

        athlete_data = {
            "athlete_id": "new_athlete",
            "name": "New Athlete",
            "first_seen_date": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        athlete = repo.create(athlete_data)

        assert athlete.id is not None
        assert athlete.athlete_id == "new_athlete"

    def test_get_or_create_existing(
        self, test_session: Session, test_athlete: Athlete
    ) -> None:
        """Test get_or_create with existing athlete."""
        repo = SQLAlchemyAthleteRepository(test_session)

        athlete_data = {
            "athlete_id": test_athlete.athlete_id,
            "name": test_athlete.name,
            "first_seen_date": datetime.now(),
        }

        athlete = repo.get_or_create(athlete_data)

        assert athlete.id == test_athlete.id

    def test_get_or_create_new(self, test_session: Session) -> None:
        """Test get_or_create with new athlete."""
        repo = SQLAlchemyAthleteRepository(test_session)

        athlete_data = {
            "athlete_id": "brand_new_athlete",
            "name": "Brand New Athlete",
            "first_seen_date": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        athlete = repo.get_or_create(athlete_data)

        assert athlete.id is not None
        assert athlete.athlete_id == "brand_new_athlete"


@pytest.mark.unit
class TestRankingRepository:
    """Test cases for SQLAlchemyRankingRepository."""

    def test_get_latest_by_epreuve(
        self, test_session: Session, test_ranking: Ranking
    ) -> None:
        """Test get latest rankings by epreuve."""
        repo = SQLAlchemyRankingRepository(test_session)

        latest_date, rankings = repo.get_latest_by_epreuve(
            test_ranking.epreuve_code, test_ranking.sexe
        )

        assert latest_date is not None
        assert len(rankings) >= 1
        assert rankings[0].epreuve_code == test_ranking.epreuve_code

    def test_create_bulk(
        self,
        test_session: Session,
        test_epreuve: Epreuve,
        test_athlete: Athlete,
    ) -> None:
        """Test bulk creating rankings."""
        repo = SQLAlchemyRankingRepository(test_session)

        rankings_data = [
            {
                "snapshot_date": datetime.now(),
                "epreuve_code": test_epreuve.code,
                "sexe": "M",
                "rank": i + 1,
                "athlete_id": f"athlete_{i}",
                "performance": f"{50 + i}m00",
                "performance_numeric": 50.0 + i,
                "club": "Test Club",
                "ligue": "I-F",
                "departement": "093",
                "created_at": datetime.now(),
            }
            for i in range(5)
        ]

        # Create athletes first
        athlete_repo = SQLAlchemyAthleteRepository(test_session)
        for data in rankings_data:
            athlete_repo.get_or_create(
                {
                    "athlete_id": data["athlete_id"],
                    "name": f"Athlete {data['rank']}",
                    "first_seen_date": datetime.now(),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )

        # Create rankings
        rankings = repo.create_bulk(rankings_data)

        assert len(rankings) == 5

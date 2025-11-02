"""Concrete implementations of repositories using SQLAlchemy."""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session

from src.core.interfaces.repositories import (
    AlertRepository,
    AthleteRepository,
    EpreuveRepository,
    FavoriteRepository,
    RankingRepository,
    ScrapeLogRepository,
    UserRepository,
)
from src.infrastructure.database.models import (
    Alert,
    Athlete,
    Epreuve,
    Favorite,
    Ranking,
    ScrapeLog,
    User,
)


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def create(self, user_data: dict[str, Any]) -> User:
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user_id: int, user_data: dict[str, Any]) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.updated_at = datetime.now()
            self.session.commit()
            self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def list_all(self) -> list[User]:
        return self.session.query(User).order_by(User.created_at.desc()).all()


class SQLAlchemyEpreuveRepository(EpreuveRepository):
    """SQLAlchemy implementation of EpreuveRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_code(self, code: int) -> Optional[Epreuve]:
        return self.session.query(Epreuve).filter(Epreuve.code == code).first()

    def get_by_id(self, epreuve_id: int) -> Optional[Epreuve]:
        return self.session.query(Epreuve).filter(Epreuve.id == epreuve_id).first()

    def list_active(self) -> list[Epreuve]:
        return self.session.query(Epreuve).filter(Epreuve.actif == True).all()

    def create(self, epreuve_data: dict[str, Any]) -> Epreuve:
        epreuve = Epreuve(**epreuve_data)
        self.session.add(epreuve)
        self.session.commit()
        self.session.refresh(epreuve)
        return epreuve

    def update(self, epreuve_id: int, epreuve_data: dict[str, Any]) -> Optional[Epreuve]:
        epreuve = self.get_by_id(epreuve_id)
        if epreuve:
            for key, value in epreuve_data.items():
                setattr(epreuve, key, value)
            epreuve.updated_at = datetime.now()
            self.session.commit()
            self.session.refresh(epreuve)
        return epreuve

    def delete(self, epreuve_id: int) -> bool:
        epreuve = self.get_by_id(epreuve_id)
        if epreuve:
            self.session.delete(epreuve)
            self.session.commit()
            return True
        return False


class SQLAlchemyAthleteRepository(AthleteRepository):
    """SQLAlchemy implementation of AthleteRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_athlete_id(self, athlete_id: str) -> Optional[Athlete]:
        return self.session.query(Athlete).filter(Athlete.athlete_id == athlete_id).first()

    def create(self, athlete_data: dict[str, Any]) -> Athlete:
        athlete = Athlete(**athlete_data)
        self.session.add(athlete)
        self.session.commit()
        self.session.refresh(athlete)
        return athlete

    def get_or_create(self, athlete_data: dict[str, Any]) -> Athlete:
        athlete = self.get_by_athlete_id(athlete_data["athlete_id"])
        if not athlete:
            athlete = self.create(athlete_data)
        return athlete


class SQLAlchemyRankingRepository(RankingRepository):
    """SQLAlchemy implementation of RankingRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_latest_by_epreuve(
        self, epreuve_code: int, sexe: str
    ) -> tuple[Optional[datetime], list[Ranking]]:
        """Get latest rankings and their snapshot date."""
        # Get latest snapshot date
        latest_date = (
            self.session.query(func.max(Ranking.snapshot_date))
            .filter(
                and_(
                    Ranking.epreuve_code == epreuve_code,
                    Ranking.sexe == sexe,
                )
            )
            .scalar()
        )

        if not latest_date:
            return None, []

        # Get rankings for latest date
        rankings = (
            self.session.query(Ranking)
            .filter(
                and_(
                    Ranking.epreuve_code == epreuve_code,
                    Ranking.sexe == sexe,
                    Ranking.snapshot_date == latest_date,
                )
            )
            .order_by(Ranking.rank)
            .all()
        )

        return latest_date, rankings

    def get_previous_rank(
        self, athlete_id: str, epreuve_code: int, sexe: str, before_date: datetime
    ) -> Optional[int]:
        """Get athlete's most recent rank before a given date."""
        ranking = (
            self.session.query(Ranking)
            .filter(
                and_(
                    Ranking.athlete_id == athlete_id,
                    Ranking.epreuve_code == epreuve_code,
                    Ranking.sexe == sexe,
                    Ranking.snapshot_date < before_date,
                )
            )
            .order_by(desc(Ranking.snapshot_date))
            .first()
        )

        return ranking.rank if ranking else None

    def create_bulk(self, rankings_data: list[dict[str, Any]]) -> list[Ranking]:
        """Create multiple rankings efficiently."""
        rankings = [Ranking(**data) for data in rankings_data]
        self.session.bulk_save_objects(rankings)
        self.session.commit()
        return rankings

    def get_athlete_history(
        self, athlete_id: str, epreuve_code: int, sexe: str, limit: int = 30
    ) -> list[Ranking]:
        """Get athlete's ranking history over time."""
        return (
            self.session.query(Ranking)
            .filter(
                and_(
                    Ranking.athlete_id == athlete_id,
                    Ranking.epreuve_code == epreuve_code,
                    Ranking.sexe == sexe,
                )
            )
            .order_by(desc(Ranking.snapshot_date))
            .limit(limit)
            .all()
        )


class SQLAlchemyFavoriteRepository(FavoriteRepository):
    """SQLAlchemy implementation of FavoriteRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_user_favorites(
        self, user_id: int, epreuve_code: Optional[int] = None
    ) -> list[Favorite]:
        query = self.session.query(Favorite).filter(Favorite.user_id == user_id)
        if epreuve_code:
            query = query.filter(Favorite.epreuve_code == epreuve_code)
        return query.order_by(desc(Favorite.added_date)).all()

    def add_favorite(self, favorite_data: dict[str, Any]) -> Favorite:
        favorite = Favorite(**favorite_data)
        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)
        return favorite

    def remove_favorite(self, user_id: int, athlete_id: str, epreuve_code: int) -> bool:
        favorite = (
            self.session.query(Favorite)
            .filter(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.athlete_id == athlete_id,
                    Favorite.epreuve_code == epreuve_code,
                )
            )
            .first()
        )
        if favorite:
            self.session.delete(favorite)
            self.session.commit()
            return True
        return False

    def is_favorite(self, user_id: int, athlete_id: str, epreuve_code: int) -> bool:
        favorite = (
            self.session.query(Favorite)
            .filter(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.athlete_id == athlete_id,
                    Favorite.epreuve_code == epreuve_code,
                )
            )
            .first()
        )
        return favorite is not None


class SQLAlchemyAlertRepository(AlertRepository):
    """SQLAlchemy implementation of AlertRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, alert_data: dict[str, Any]) -> Alert:
        alert = Alert(**alert_data)
        self.session.add(alert)
        self.session.commit()
        self.session.refresh(alert)
        return alert

    def create_bulk(self, alerts_data: list[dict[str, Any]]) -> list[Alert]:
        alerts = [Alert(**data) for data in alerts_data]
        self.session.bulk_save_objects(alerts)
        self.session.commit()
        return alerts

    def get_user_alerts(
        self, user_id: int, is_read: Optional[bool] = None, limit: int = 50
    ) -> list[Alert]:
        query = self.session.query(Alert).filter(Alert.user_id == user_id)
        if is_read is not None:
            query = query.filter(Alert.is_read == is_read)
        return query.order_by(desc(Alert.created_at)).limit(limit).all()

    def mark_as_read(self, alert_id: int) -> bool:
        alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.is_read = True
            self.session.commit()
            return True
        return False

    def mark_all_as_read(self, user_id: int) -> int:
        count = (
            self.session.query(Alert)
            .filter(and_(Alert.user_id == user_id, Alert.is_read == False))
            .update({Alert.is_read: True})
        )
        self.session.commit()
        return count

    def count_unread(self, user_id: int) -> int:
        return (
            self.session.query(Alert)
            .filter(and_(Alert.user_id == user_id, Alert.is_read == False))
            .count()
        )


class SQLAlchemyScrapeLogRepository(ScrapeLogRepository):
    """SQLAlchemy implementation of ScrapeLogRepository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, log_data: dict[str, Any]) -> ScrapeLog:
        log = ScrapeLog(**log_data)
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log

    def get_recent_logs(
        self, epreuve_code: Optional[int] = None, limit: int = 50
    ) -> list[ScrapeLog]:
        query = self.session.query(ScrapeLog)
        if epreuve_code:
            query = query.filter(ScrapeLog.epreuve_code == epreuve_code)
        return query.order_by(desc(ScrapeLog.scrape_date)).limit(limit).all()

    def get_last_success(self, epreuve_code: int, sexe: str) -> Optional[ScrapeLog]:
        return (
            self.session.query(ScrapeLog)
            .filter(
                and_(
                    ScrapeLog.epreuve_code == epreuve_code,
                    ScrapeLog.sexe == sexe,
                    ScrapeLog.status == "success",
                )
            )
            .order_by(desc(ScrapeLog.scrape_date))
            .first()
        )

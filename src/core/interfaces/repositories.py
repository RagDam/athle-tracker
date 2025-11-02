"""Repository interfaces for clean architecture."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from src.infrastructure.database.models import (
    Alert,
    Athlete,
    Epreuve,
    Favorite,
    Ranking,
    ScrapeLog,
    User,
)


class UserRepository(ABC):
    """Interface for User repository."""

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    def create(self, user_data: dict[str, Any]) -> User:
        """Create new user."""
        pass

    @abstractmethod
    def update(self, user_id: int, user_data: dict[str, Any]) -> Optional[User]:
        """Update user."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        """List all users."""
        pass


class EpreuveRepository(ABC):
    """Interface for Epreuve repository."""

    @abstractmethod
    def get_by_code(self, code: int) -> Optional[Epreuve]:
        """Get epreuve by code."""
        pass

    @abstractmethod
    def get_by_id(self, epreuve_id: int) -> Optional[Epreuve]:
        """Get epreuve by ID."""
        pass

    @abstractmethod
    def list_active(self) -> list[Epreuve]:
        """List all active epreuves."""
        pass

    @abstractmethod
    def create(self, epreuve_data: dict[str, Any]) -> Epreuve:
        """Create new epreuve."""
        pass

    @abstractmethod
    def update(self, epreuve_id: int, epreuve_data: dict[str, Any]) -> Optional[Epreuve]:
        """Update epreuve."""
        pass

    @abstractmethod
    def delete(self, epreuve_id: int) -> bool:
        """Delete epreuve."""
        pass


class AthleteRepository(ABC):
    """Interface for Athlete repository."""

    @abstractmethod
    def get_by_athlete_id(self, athlete_id: str) -> Optional[Athlete]:
        """Get athlete by athlete_id."""
        pass

    @abstractmethod
    def create(self, athlete_data: dict[str, Any]) -> Athlete:
        """Create new athlete."""
        pass

    @abstractmethod
    def get_or_create(self, athlete_data: dict[str, Any]) -> Athlete:
        """Get or create athlete."""
        pass


class RankingRepository(ABC):
    """Interface for Ranking repository."""

    @abstractmethod
    def get_latest_by_epreuve(
        self, epreuve_code: int, sexe: str
    ) -> tuple[Optional[datetime], list[Ranking]]:
        """Get latest rankings for an epreuve and gender."""
        pass

    @abstractmethod
    def get_previous_rank(
        self, athlete_id: str, epreuve_code: int, sexe: str, before_date: datetime
    ) -> Optional[int]:
        """Get athlete's previous rank."""
        pass

    @abstractmethod
    def create_bulk(self, rankings_data: list[dict[str, Any]]) -> list[Ranking]:
        """Create multiple rankings."""
        pass

    @abstractmethod
    def get_athlete_history(
        self, athlete_id: str, epreuve_code: int, sexe: str, limit: int = 30
    ) -> list[Ranking]:
        """Get athlete's ranking history."""
        pass


class FavoriteRepository(ABC):
    """Interface for Favorite repository."""

    @abstractmethod
    def get_user_favorites(self, user_id: int, epreuve_code: Optional[int] = None) -> list[Favorite]:
        """Get user's favorites."""
        pass

    @abstractmethod
    def add_favorite(self, favorite_data: dict[str, Any]) -> Favorite:
        """Add favorite."""
        pass

    @abstractmethod
    def remove_favorite(self, user_id: int, athlete_id: str, epreuve_code: int) -> bool:
        """Remove favorite."""
        pass

    @abstractmethod
    def is_favorite(self, user_id: int, athlete_id: str, epreuve_code: int) -> bool:
        """Check if athlete is favorite."""
        pass


class AlertRepository(ABC):
    """Interface for Alert repository."""

    @abstractmethod
    def create(self, alert_data: dict[str, Any]) -> Alert:
        """Create alert."""
        pass

    @abstractmethod
    def create_bulk(self, alerts_data: list[dict[str, Any]]) -> list[Alert]:
        """Create multiple alerts."""
        pass

    @abstractmethod
    def get_user_alerts(
        self, user_id: int, is_read: Optional[bool] = None, limit: int = 50
    ) -> list[Alert]:
        """Get user's alerts."""
        pass

    @abstractmethod
    def mark_as_read(self, alert_id: int) -> bool:
        """Mark alert as read."""
        pass

    @abstractmethod
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all user's alerts as read."""
        pass

    @abstractmethod
    def count_unread(self, user_id: int) -> int:
        """Count unread alerts."""
        pass


class ScrapeLogRepository(ABC):
    """Interface for ScrapeLog repository."""

    @abstractmethod
    def create(self, log_data: dict[str, Any]) -> ScrapeLog:
        """Create scrape log."""
        pass

    @abstractmethod
    def get_recent_logs(self, epreuve_code: Optional[int] = None, limit: int = 50) -> list[ScrapeLog]:
        """Get recent scrape logs."""
        pass

    @abstractmethod
    def get_last_success(self, epreuve_code: int, sexe: str) -> Optional[ScrapeLog]:
        """Get last successful scrape."""
        pass

"""SQLAlchemy database models."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default="user"
    )  # user or admin
    actif: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user", cascade="all, delete-orphan"
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


class Epreuve(Base):
    """Competition event model (e.g., Javelin, Shot Put, Discus)."""

    __tablename__ = "epreuves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    actif: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    # Relationships
    rankings: Mapped[list["Ranking"]] = relationship(
        "Ranking", back_populates="epreuve", cascade="all, delete-orphan"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="epreuve", cascade="all, delete-orphan"
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert", back_populates="epreuve", cascade="all, delete-orphan"
    )
    scrape_logs: Mapped[list["ScrapeLog"]] = relationship(
        "ScrapeLog", back_populates="epreuve", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Epreuve(id={self.id}, nom='{self.nom}', code={self.code})>"


class Athlete(Base):
    """Athlete model to track individual athletes."""

    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    athlete_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    first_seen_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    # Relationships
    rankings: Mapped[list["Ranking"]] = relationship(
        "Ranking", back_populates="athlete", cascade="all, delete-orphan"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="athlete", cascade="all, delete-orphan"
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert", back_populates="athlete", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Athlete(id={self.id}, name='{self.name}', athlete_id='{self.athlete_id}')>"


class Ranking(Base):
    """Ranking snapshot for a specific date, event, and gender."""

    __tablename__ = "rankings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    epreuve_code: Mapped[int] = mapped_column(
        Integer, ForeignKey("epreuves.code", ondelete="CASCADE"), nullable=False, index=True
    )
    sexe: Mapped[str] = mapped_column(String(1), nullable=False, index=True)  # M or F
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    athlete_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("athletes.athlete_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    performance: Mapped[str] = mapped_column(String(50), nullable=False)
    performance_numeric: Mapped[float] = mapped_column(Float, nullable=False)
    club: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ligue: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    departement: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )

    # Relationships
    epreuve: Mapped["Epreuve"] = relationship("Epreuve", back_populates="rankings")
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="rankings")

    # Indexes for common queries
    __table_args__ = (
        Index("idx_ranking_date_epreuve_sexe", "snapshot_date", "epreuve_code", "sexe"),
        Index("idx_ranking_athlete_epreuve", "athlete_id", "epreuve_code"),
    )

    def __repr__(self) -> str:
        return f"<Ranking(id={self.id}, rank={self.rank}, athlete_id='{self.athlete_id}', performance='{self.performance}')>"


class Favorite(Base):
    """User's favorite athletes for a specific event."""

    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    athlete_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("athletes.athlete_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    epreuve_code: Mapped[int] = mapped_column(
        Integer, ForeignKey("epreuves.code", ondelete="CASCADE"), nullable=False, index=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    added_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="favorites")
    epreuve: Mapped["Epreuve"] = relationship("Epreuve", back_populates="favorites")

    # Unique constraint: one favorite per user/athlete/epreuve combination
    __table_args__ = (Index("idx_favorite_user_athlete_epreuve", "user_id", "athlete_id", "epreuve_code", unique=True),)

    def __repr__(self) -> str:
        return f"<Favorite(id={self.id}, user_id={self.user_id}, athlete_id='{self.athlete_id}')>"


class Alert(Base):
    """Alert model for ranking changes and favorites."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now(), index=True
    )
    alert_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # critique, important, info
    athlete_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("athletes.athlete_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    epreuve_code: Mapped[int] = mapped_column(
        Integer, ForeignKey("epreuves.code", ondelete="CASCADE"), nullable=False, index=True
    )
    sexe: Mapped[str] = mapped_column(String(1), nullable=False)  # M or F
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    old_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    new_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="alerts")
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="alerts")
    epreuve: Mapped["Epreuve"] = relationship("Epreuve", back_populates="alerts")

    # Index for filtering unread alerts
    __table_args__ = (Index("idx_alert_user_read", "user_id", "is_read"),)

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, alert_type='{self.alert_type}', title='{self.title}', is_read={self.is_read})>"


class ScrapeLog(Base):
    """Log model for scraping operations."""

    __tablename__ = "scrape_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scrape_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now(), index=True
    )
    epreuve_code: Mapped[int] = mapped_column(
        Integer, ForeignKey("epreuves.code", ondelete="CASCADE"), nullable=False, index=True
    )
    sexe: Mapped[str] = mapped_column(String(1), nullable=False)  # M or F
    status: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # success, error, partial
    results_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )

    # Relationships
    epreuve: Mapped["Epreuve"] = relationship("Epreuve", back_populates="scrape_logs")

    # Index for filtering logs by date and event
    __table_args__ = (Index("idx_scrape_log_date_epreuve", "scrape_date", "epreuve_code"),)

    def __repr__(self) -> str:
        return f"<ScrapeLog(id={self.id}, epreuve_code={self.epreuve_code}, status='{self.status}', results_count={self.results_count})>"

"""Core interfaces package."""

from .repositories import (
    AlertRepository,
    AthleteRepository,
    EpreuveRepository,
    FavoriteRepository,
    RankingRepository,
    ScrapeLogRepository,
    UserRepository,
)

__all__ = [
    "UserRepository",
    "EpreuveRepository",
    "AthleteRepository",
    "RankingRepository",
    "FavoriteRepository",
    "AlertRepository",
    "ScrapeLogRepository",
]

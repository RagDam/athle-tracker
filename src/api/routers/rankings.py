"""Rankings endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.api.dependencies import get_db, get_current_user
from src.api.schemas import RankingResponse
from src.infrastructure.database.repositories import SQLAlchemyRankingRepository

router = APIRouter(prefix="/rankings", tags=["Rankings"])


@router.get("/", response_model=list[RankingResponse])
def get_rankings(
    epreuve_code: Annotated[int, Query(ge=1)],
    sexe: Annotated[str, Query(pattern="^[MF]$")] = "M",
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None,
) -> list[RankingResponse]:
    """
    Get latest rankings for an event.

    Args:
        epreuve_code: Event code
        sexe: Gender (M or F)
        db: Database session
        current_user: Authenticated user

    Returns:
        List of rankings
    """
    ranking_repo = SQLAlchemyRankingRepository(db)
    latest_date, rankings = ranking_repo.get_latest_by_epreuve(epreuve_code, sexe)

    if not rankings:
        return []

    return [RankingResponse.model_validate(r) for r in rankings]


@router.get("/all", response_model=list[RankingResponse])
def get_all_rankings(
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None,
) -> list[RankingResponse]:
    """
    Get latest rankings for the first active event.
    This is a convenience endpoint that returns all rankings without requiring epreuve_code.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        List of rankings from the first active event, or empty list if none found
    """
    from src.infrastructure.database.models import Epreuve

    # Get first active epreuve
    epreuve = db.query(Epreuve).filter_by(actif=True).first()

    if not epreuve:
        return []

    ranking_repo = SQLAlchemyRankingRepository(db)
    # Use epreuve.code (670) not epreuve.id (1) - rankings are stored with code
    latest_date, rankings = ranking_repo.get_latest_by_epreuve(epreuve.code, "M")

    if not rankings:
        return []

    # Map database model to response schema with correct field names
    return [
        RankingResponse(
            id=r.id,
            epreuve_code=r.epreuve_code,
            athlete_id=r.athlete_id,
            sexe=r.sexe,
            rang=r.rank,  # Map "rank" to "rang"
            athlete_nom=r.athlete.name,  # Map "athlete.name" to "athlete_nom"
            performance=r.performance,
            performance_numeric=r.performance_numeric,
            club=r.club,
            ligue=r.ligue,
            departement=r.departement,
            date_performance=r.snapshot_date,  # Use snapshot_date for date_performance
            date_scraping=r.snapshot_date,  # Use snapshot_date for date_scraping
            changement_rang=0,  # TODO: Calculate rank changes
        )
        for r in rankings
    ]


@router.get("/podium", response_model=list[RankingResponse])
def get_podium(
    epreuve_code: Annotated[int, Query(ge=1)],
    sexe: Annotated[str, Query(pattern="^[MF]$")] = "M",
    limit: Annotated[int, Query(ge=1, le=10)] = 3,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None,
) -> list[RankingResponse]:
    """
    Get top N rankings (podium) for an event.

    Args:
        epreuve_code: Event code
        sexe: Gender (M or F)
        limit: Number of top athletes to return (default 3)
        db: Database session
        current_user: Authenticated user

    Returns:
        List of top rankings
    """
    ranking_repo = SQLAlchemyRankingRepository(db)
    latest_date, rankings = ranking_repo.get_latest_by_epreuve(epreuve_code, sexe)

    if not rankings:
        return []

    return [RankingResponse.model_validate(r) for r in rankings[:limit]]

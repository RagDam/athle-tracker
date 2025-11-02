"""Scraping endpoints (admin only)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.api.dependencies import get_db, get_current_admin_user
from src.api.schemas import (
    ScrapeRequest,
    ScrapeResultResponse,
    ScrapeLogResponse,
)
from src.infrastructure.database.repositories import SQLAlchemyScrapeLogRepository
from src.infrastructure.scheduler.scraping_scheduler import ScrapingScheduler

router = APIRouter(prefix="/scraping", tags=["Scraping"])


@router.post("/manual", response_model=ScrapeResultResponse)
def run_manual_scrape(
    data: ScrapeRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> ScrapeResultResponse:
    """
    Run manual scraping for an event (admin only).

    Args:
        data: Scrape request (epreuve_code + sexe)
        db: Database session
        current_user: Authenticated admin user

    Returns:
        Scraping result
    """
    scheduler = ScrapingScheduler()
    result = scheduler.run_manual_scrape(data.epreuve_code, data.sexe)

    return ScrapeResultResponse(**result)


@router.get("/logs", response_model=list[ScrapeLogResponse])
def get_scrape_logs(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_admin_user)] = None,
) -> list[ScrapeLogResponse]:
    """
    Get recent scrape logs (admin only).

    Args:
        limit: Maximum number of logs to return
        db: Database session
        current_user: Authenticated admin user

    Returns:
        List of scrape logs
    """
    log_repo = SQLAlchemyScrapeLogRepository(db)
    logs = log_repo.get_recent_logs(limit)

    return [ScrapeLogResponse.model_validate(log) for log in logs]


@router.get("/scheduler/status")
def get_scheduler_status(
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> dict:
    """
    Get scheduler status (admin only).

    Args:
        current_user: Authenticated admin user

    Returns:
        Scheduler status information
    """
    scheduler = ScrapingScheduler()
    next_run = scheduler.get_next_run_time()

    return {
        "enabled": True,  # From settings
        "next_run_time": next_run,
    }

"""Alerts endpoints."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.api.dependencies import get_db, get_current_user
from src.api.schemas import AlertResponse
from src.infrastructure.database.repositories import SQLAlchemyAlertRepository

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=list[AlertResponse])
def get_user_alerts(
    is_read: Annotated[Optional[bool], Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None,
) -> list[AlertResponse]:
    """
    Get alerts for current user.

    Args:
        is_read: Filter by read status (None = all)
        limit: Maximum number of alerts to return
        db: Database session
        current_user: Authenticated user

    Returns:
        List of alerts
    """
    alert_repo = SQLAlchemyAlertRepository(db)
    alerts = alert_repo.get_user_alerts(current_user["id"], is_read, limit)

    return [AlertResponse.model_validate(a) for a in alerts]


@router.get("/unread-count", response_model=int)
def get_unread_count(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> int:
    """
    Get count of unread alerts for current user.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        Number of unread alerts
    """
    alert_repo = SQLAlchemyAlertRepository(db)
    return alert_repo.count_unread(current_user["id"])


@router.patch("/{alert_id}/read")
def mark_alert_as_read(
    alert_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """
    Mark an alert as read.

    Args:
        alert_id: Alert ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Success message

    Raises:
        HTTPException: If alert not found or doesn't belong to user
    """
    alert_repo = SQLAlchemyAlertRepository(db)
    alert = alert_repo.get_by_id(alert_id)

    if not alert or alert.user_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert_repo.mark_as_read(alert_id)

    return {"message": "Alert marked as read"}


@router.patch("/mark-all-read")
def mark_all_alerts_as_read(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """
    Mark all alerts as read for current user.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        Count of marked alerts
    """
    alert_repo = SQLAlchemyAlertRepository(db)
    count = alert_repo.mark_all_as_read(current_user["id"])

    return {"message": f"{count} alerts marked as read", "count": count}

"""Epreuves (Events) endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies import get_db, get_current_user, get_current_admin_user
from src.api.schemas import EpreuveResponse, EpreuveCreate, EpreuveUpdate
from src.infrastructure.database.repositories import SQLAlchemyEpreuveRepository
from src.infrastructure.database.models import Epreuve

router = APIRouter(prefix="/epreuves", tags=["Epreuves"])


@router.get("/", response_model=list[EpreuveResponse])
def get_all_epreuves(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[EpreuveResponse]:
    """
    Get all epreuves.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        List of all epreuves
    """
    epreuve_repo = SQLAlchemyEpreuveRepository(db)
    epreuves = epreuve_repo.list_all()

    return [EpreuveResponse.model_validate(e) for e in epreuves]


@router.get("/active", response_model=list[EpreuveResponse])
def get_active_epreuves(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> list[EpreuveResponse]:
    """
    Get active epreuves only.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        List of active epreuves
    """
    epreuve_repo = SQLAlchemyEpreuveRepository(db)
    epreuves = epreuve_repo.list_active()

    return [EpreuveResponse.model_validate(e) for e in epreuves]


@router.get("/{epreuve_id}", response_model=EpreuveResponse)
def get_epreuve(
    epreuve_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EpreuveResponse:
    """
    Get epreuve by ID.

    Args:
        epreuve_id: Epreuve ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Epreuve details

    Raises:
        HTTPException: If epreuve not found
    """
    epreuve_repo = SQLAlchemyEpreuveRepository(db)
    epreuve = epreuve_repo.get_by_id(epreuve_id)

    if not epreuve:
        raise HTTPException(status_code=404, detail="Epreuve not found")

    return EpreuveResponse.model_validate(epreuve)


@router.post("/", response_model=EpreuveResponse, status_code=201)
def create_epreuve(
    data: EpreuveCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> EpreuveResponse:
    """
    Create new epreuve (admin only).

    Args:
        data: Epreuve data
        db: Database session
        current_user: Authenticated admin user

    Returns:
        Created epreuve

    Raises:
        HTTPException: If epreuve code already exists
    """
    epreuve_repo = SQLAlchemyEpreuveRepository(db)

    # Check if code already exists
    existing = epreuve_repo.get_by_code(data.code)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Epreuve with code {data.code} already exists",
        )

    epreuve = Epreuve(
        code=data.code,
        nom=data.nom,
        is_active=data.is_active,
    )

    created = epreuve_repo.create(epreuve)

    return EpreuveResponse.model_validate(created)


@router.patch("/{epreuve_id}", response_model=EpreuveResponse)
def update_epreuve(
    epreuve_id: int,
    data: EpreuveUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> EpreuveResponse:
    """
    Update epreuve (admin only).

    Args:
        epreuve_id: Epreuve ID
        data: Update data
        db: Database session
        current_user: Authenticated admin user

    Returns:
        Updated epreuve

    Raises:
        HTTPException: If epreuve not found
    """
    epreuve_repo = SQLAlchemyEpreuveRepository(db)
    epreuve = epreuve_repo.get_by_id(epreuve_id)

    if not epreuve:
        raise HTTPException(status_code=404, detail="Epreuve not found")

    # Update fields if provided
    if data.nom is not None:
        epreuve.nom = data.nom
    if data.is_active is not None:
        epreuve.is_active = data.is_active

    updated = epreuve_repo.update(epreuve)

    return EpreuveResponse.model_validate(updated)


@router.delete("/{epreuve_id}", status_code=204)
def delete_epreuve(
    epreuve_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> None:
    """
    Delete epreuve (admin only).

    Args:
        epreuve_id: Epreuve ID
        db: Database session
        current_user: Authenticated admin user

    Raises:
        HTTPException: If epreuve not found
    """
    epreuve_repo = SQLAlchemyEpreuveRepository(db)
    epreuve = epreuve_repo.get_by_id(epreuve_id)

    if not epreuve:
        raise HTTPException(status_code=404, detail="Epreuve not found")

    epreuve_repo.delete(epreuve_id)

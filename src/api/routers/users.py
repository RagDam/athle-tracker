"""User management endpoints (admin only)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies import (
    get_db,
    get_current_admin_user,
    get_password_hash,
)
from src.api.schemas import UserResponse, UserCreate, UserUpdate
from src.infrastructure.database.repositories import SQLAlchemyUserRepository
from src.infrastructure.database.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> list[UserResponse]:
    """
    Get all users (admin only).

    Args:
        db: Database session
        current_user: Authenticated admin user

    Returns:
        List of all users
    """
    user_repo = SQLAlchemyUserRepository(db)
    users = user_repo.list_all()

    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> UserResponse:
    """
    Get user by ID (admin only).

    Args:
        user_id: User ID
        db: Database session
        current_user: Authenticated admin user

    Returns:
        User details

    Raises:
        HTTPException: If user not found
    """
    user_repo = SQLAlchemyUserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> UserResponse:
    """
    Create new user (admin only).

    Args:
        data: User data
        db: Database session
        current_user: Authenticated admin user

    Returns:
        Created user

    Raises:
        HTTPException: If email already exists
    """
    user_repo = SQLAlchemyUserRepository(db)

    # Check if email already exists
    existing = user_repo.get_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user_data = {
        "email": data.email,
        "password_hash": get_password_hash(data.password),
        "role": data.role,
    }

    created = user_repo.create(user_data)

    return UserResponse.model_validate(created)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> UserResponse:
    """
    Update user (admin only).

    Args:
        user_id: User ID
        data: Update data
        db: Database session
        current_user: Authenticated admin user

    Returns:
        Updated user

    Raises:
        HTTPException: If user not found or email already exists
    """
    user_repo = SQLAlchemyUserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check email uniqueness if changing email
    if data.email and data.email != user.email:
        existing = user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

    # Build update data
    update_data = {}
    if data.email and data.email != user.email:
        update_data["email"] = data.email
    if data.password:
        update_data["password_hash"] = get_password_hash(data.password)
    if data.role:
        update_data["role"] = data.role

    updated = user_repo.update(user_id, update_data)

    return UserResponse.model_validate(updated)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_admin_user)],
) -> None:
    """
    Delete user (admin only).

    Args:
        user_id: User ID
        db: Database session
        current_user: Authenticated admin user

    Raises:
        HTTPException: If user not found or trying to delete self
    """
    user_repo = SQLAlchemyUserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent deleting own account
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account",
        )

    user_repo.delete(user_id)

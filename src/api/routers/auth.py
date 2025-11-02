"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import (
    get_db,
    get_password_hash,
    verify_password,
    create_access_token,
)
from src.api.schemas import LoginRequest, LoginResponse, UserResponse
from src.infrastructure.database.repositories import SQLAlchemyUserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LoginResponse:
    """
    Authenticate user and return JWT token.

    Args:
        credentials: Login credentials (email + password)
        db: Database session

    Returns:
        JWT token and user info

    Raises:
        HTTPException: If credentials are invalid
    """
    user_repo = SQLAlchemyUserRepository(db)
    user = user_repo.get_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token (sub must be a string, not int)
    access_token = create_access_token(data={"sub": str(user.id)})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )

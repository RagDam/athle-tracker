"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# Authentication
# ============================================================================

class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response schema."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response schema."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============================================================================
# Athletes
# ============================================================================

class AthleteResponse(BaseModel):
    """Athlete response schema."""

    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Epreuves (Events)
# ============================================================================

class EpreuveResponse(BaseModel):
    """Epreuve response schema."""

    id: int
    code: int
    nom: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EpreuveCreate(BaseModel):
    """Create epreuve request schema."""

    code: int = Field(..., ge=1, description="Epreuve code (must be positive)")
    nom: str = Field(..., min_length=1, description="Epreuve name")
    is_active: bool = True


class EpreuveUpdate(BaseModel):
    """Update epreuve request schema."""

    nom: Optional[str] = Field(None, min_length=1)
    is_active: Optional[bool] = None


# ============================================================================
# Rankings
# ============================================================================

class RankingResponse(BaseModel):
    """Ranking response schema."""

    id: int
    epreuve_code: int
    athlete_id: str
    sexe: str
    rang: int  # Frontend expects "rang" not "rank"
    athlete_nom: str  # Frontend expects "athlete_nom"
    performance: str
    performance_numeric: float
    club: Optional[str]
    ligue: Optional[str]
    departement: Optional[str]
    date_performance: datetime  # Frontend expects "date_performance"
    date_scraping: datetime  # Frontend expects "date_scraping"
    changement_rang: int = 0  # Rank change indicator

    class Config:
        from_attributes = True


# ============================================================================
# Alerts
# ============================================================================

class AlertResponse(BaseModel):
    """Alert response schema."""

    id: int
    user_id: int
    alert_type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Scraping
# ============================================================================

class ScrapeRequest(BaseModel):
    """Manual scraping request schema."""

    epreuve_code: int = Field(..., ge=1)
    sexe: str = Field(..., pattern="^[MF]$")


class ScrapeResultResponse(BaseModel):
    """Scraping result response schema."""

    success: bool
    rankings_count: int = 0
    alerts_count: int = 0
    duration_seconds: float
    error: Optional[str] = None


class ScrapeLogResponse(BaseModel):
    """Scrape log response schema."""

    id: int
    epreuve_code: int
    sexe: str
    scrape_date: datetime
    status: str
    results_count: int
    duration_seconds: float
    error_message: Optional[str]

    class Config:
        from_attributes = True


# ============================================================================
# Users (Admin)
# ============================================================================

class UserCreate(BaseModel):
    """Create user request schema."""

    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", pattern="^(admin|user)$")


class UserUpdate(BaseModel):
    """Update user request schema."""

    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = Field(None, pattern="^(admin|user)$")

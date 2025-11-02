"""Application configuration."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database
DATABASE_PATH = BASE_DIR / "athle_tracker.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Security
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "your-secret-key-change-in-production-please-use-a-strong-random-key",
)
JWT_ALGORITHM = "HS256"

# Scheduler
SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "true").lower() == "true"
SCHEDULER_START_HOUR = int(os.getenv("SCHEDULER_START_HOUR", "1"))
SCHEDULER_START_MINUTE = int(os.getenv("SCHEDULER_START_MINUTE", "45"))
SCHEDULER_END_HOUR = int(os.getenv("SCHEDULER_END_HOUR", "3"))
SCHEDULER_END_MINUTE = int(os.getenv("SCHEDULER_END_MINUTE", "15"))
TIMEZONE = "Europe/Paris"


class Settings:
    """Application settings."""

    def __init__(self):
        self.database_url = DATABASE_URL
        self.jwt_secret_key = JWT_SECRET_KEY
        self.jwt_algorithm = JWT_ALGORITHM
        self.scheduler_enabled = SCHEDULER_ENABLED
        self.scheduler_start_hour = SCHEDULER_START_HOUR
        self.scheduler_start_minute = SCHEDULER_START_MINUTE
        self.scheduler_end_hour = SCHEDULER_END_HOUR
        self.scheduler_end_minute = SCHEDULER_END_MINUTE
        self.timezone = TIMEZONE


settings = Settings()

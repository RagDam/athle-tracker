"""Application configuration using Pydantic Settings."""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="sqlite:///./athle_tracker.db",
        description="Database connection URL",
    )

    # Application
    app_name: str = Field(default="Athle Tracker", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Scraping Configuration
    scraping_min_delay: float = Field(
        default=2.0,
        description="Minimum delay between requests (seconds)",
    )
    scraping_max_delay: float = Field(
        default=3.0,
        description="Maximum delay between requests (seconds)",
    )
    scraping_max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts",
    )
    scraping_timeout: int = Field(
        default=30,
        description="Request timeout (seconds)",
    )

    # Scheduler Configuration
    scheduler_enabled: bool = Field(
        default=True,
        description="Enable automatic scraping scheduler",
    )
    scheduler_start_hour: int = Field(
        default=1,
        description="Scheduler start hour (24h format)",
    )
    scheduler_start_minute: int = Field(
        default=45,
        description="Scheduler start minute",
    )
    scheduler_end_hour: int = Field(
        default=3,
        description="Scheduler end hour (24h format)",
    )
    scheduler_end_minute: int = Field(
        default=15,
        description="Scheduler end minute",
    )
    timezone: str = Field(
        default="Europe/Paris",
        description="Timezone for scheduler",
    )

    # Security
    secret_key: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT encoding",
    )
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production-please-use-a-strong-random-key",
        description="JWT secret key",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT algorithm",
    )
    cookie_name: str = Field(
        default="athle_tracker_auth",
        description="Authentication cookie name",
    )
    cookie_expiry_days: int = Field(
        default=30,
        description="Cookie expiration in days",
    )

    # Admin Default Credentials
    admin_email: str = Field(
        default="admin@example.com",
        description="Default admin email",
    )
    admin_password: str = Field(
        default="admin123",
        description="Default admin password",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(
        default="logs/athle_tracker.log",
        description="Log file path",
    )
    log_max_bytes: int = Field(
        default=10485760,
        description="Maximum log file size (bytes)",
    )
    log_backup_count: int = Field(
        default=5,
        description="Number of log backup files",
    )

    # Athle.fr URLs
    athle_base_url: str = Field(
        default="https://www.athle.fr/bases/liste.aspx",
        description="Base URL for athle.fr rankings",
    )

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent

    @property
    def logs_dir(self) -> Path:
        """Get logs directory."""
        logs_path = self.project_root / "logs"
        logs_path.mkdir(exist_ok=True)
        return logs_path


# Global settings instance
settings = Settings()

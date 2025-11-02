"""Database initialization script with default data."""

from datetime import datetime

from passlib.hash import bcrypt

from src.config import settings
from src.infrastructure.database.connection import SessionLocal, init_db
from src.infrastructure.database.models import Epreuve, User
from src.utils import logger


def create_default_data() -> None:
    """Create default admin user and Javelot event."""
    session = SessionLocal()

    try:
        logger.info("Creating default data...")

        # Check if admin user already exists
        existing_admin = session.query(User).filter_by(email=settings.admin_email).first()
        if not existing_admin:
            # Create default admin user
            admin_user = User(
                email=settings.admin_email,
                password_hash=bcrypt.hash(settings.admin_password),
                role="admin",
                actif=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(admin_user)
            logger.info(f"Created admin user: {settings.admin_email}")
        else:
            logger.info(f"Admin user already exists: {settings.admin_email}")

        # Check if Javelot event already exists
        existing_javelot = session.query(Epreuve).filter_by(code=670).first()
        if not existing_javelot:
            # Create Javelot event
            javelot = Epreuve(
                nom="Javelot",
                code=670,
                actif=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(javelot)
            logger.info("Created Javelot event (code 670)")
        else:
            logger.info("Javelot event already exists (code 670)")

        session.commit()
        logger.info("Default data created successfully")

    except Exception as e:
        logger.error(f"Failed to create default data: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def main() -> None:
    """Main initialization function."""
    try:
        logger.info("Starting database initialization...")

        # Create tables
        init_db()

        # Create default data
        create_default_data()

        logger.info("Database initialization completed successfully")
        logger.info(f"Admin credentials: {settings.admin_email} / {settings.admin_password}")
        logger.warning("⚠️  Please change admin password after first login!")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()

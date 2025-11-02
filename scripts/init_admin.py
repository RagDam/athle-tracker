"""
Script to initialize database with default admin user.

Usage:
    python scripts/init_admin.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from passlib.context import CryptContext
from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.database.models import User
from src.infrastructure.database.repositories import SQLAlchemyUserRepository

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin_user(
    email: str = "admin@test.com",
    password: str = "admin123",
    role: str = "admin"
) -> None:
    """
    Create default admin user if it doesn't exist.

    Args:
        email: Admin email
        password: Admin password
        role: User role (default: admin)
    """
    session = SessionLocal()

    try:
        user_repo = SQLAlchemyUserRepository(session)

        # Check if admin already exists
        existing_user = user_repo.get_by_email(email)

        if existing_user:
            print(f"[OK] User {email} already exists (ID: {existing_user.id})")
            print(f"  Role: {existing_user.role}")
            return

        # Create new admin user
        user_data = {
            "email": email,
            "password_hash": pwd_context.hash(password),
            "role": role,
            "actif": True,
        }

        user = user_repo.create(user_data)

        print(f"[OK] Admin user created successfully!")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  Password: {password}")
        print()
        print("You can now login with:")
        print(f"  Email: {email}")
        print(f"  Password: {password}")

    except Exception as e:
        print(f"[ERROR] Error creating admin user: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def create_test_user(
    email: str = "user@test.com",
    password: str = "user123",
    role: str = "user"
) -> None:
    """
    Create default test user if it doesn't exist.

    Args:
        email: User email
        password: User password
        role: User role (default: user)
    """
    session = SessionLocal()

    try:
        user_repo = SQLAlchemyUserRepository(session)

        # Check if user already exists
        existing_user = user_repo.get_by_email(email)

        if existing_user:
            print(f"[OK] User {email} already exists (ID: {existing_user.id})")
            return

        # Create new test user
        user_data = {
            "email": email,
            "password_hash": pwd_context.hash(password),
            "role": role,
            "actif": True,
        }

        user = user_repo.create(user_data)

        print(f"[OK] Test user created successfully!")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")

    except Exception as e:
        print(f"[ERROR] Error creating test user: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Athle Tracker - Database Initialization")
    print("=" * 60)
    print()

    # Create admin user
    create_admin_user(
        email="admin@test.com",
        password="admin123",
        role="admin"
    )

    print()

    # Create regular test user
    create_test_user(
        email="user@test.com",
        password="user123",
        role="user"
    )

    print()
    print("=" * 60)
    print("Initialization complete!")
    print("=" * 60)

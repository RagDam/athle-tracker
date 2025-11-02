"""Initialize a sample competition and run scraping to populate data."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.database.models import Epreuve
from src.infrastructure.database.repositories import SQLAlchemyEpreuveRepository
from src.core.use_cases.scrape_rankings import ScrapeRankingsUseCase
from src.infrastructure.scraping.athle_scraper import AthleScraper


def create_sample_epreuve():
    """Create a sample competition (Javelot Cadets 2026)."""
    session = SessionLocal()
    try:
        repo = SQLAlchemyEpreuveRepository(session)

        # Check if epreuve already exists
        existing = session.query(Epreuve).filter_by(nom="Javelot Cadets 2026").first()

        if existing:
            print(f"[OK] Epreuve '{existing.nom}' already exists (ID: {existing.id})")
            return existing.id

        # Create new epreuve
        epreuve_data = {
            "nom": "Javelot Cadets 2026",
            "discipline": "Javelot",
            "categorie": "CA",
            "annee": 2026,
            "url": "https://www.athle.fr/bases/liste.aspx?frmposition=1&frmbase=records&frmmode=1&frmespace=0&frmsaison=2026&frmepreuve=JAV&frmgenre=M&frmcategorie=CA&frmnbres=200",
            "active": True,
        }

        epreuve = repo.create(epreuve_data)
        print(f"[OK] Created epreuve: {epreuve.nom} (ID: {epreuve.id})")
        print(f"  URL: {epreuve.url}")
        return epreuve.id

    except Exception as e:
        print(f"[ERROR] Failed to create epreuve: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def run_scraping(epreuve_id: int):
    """Run scraping for the specified competition."""
    session = SessionLocal()
    try:
        print("\n" + "=" * 60)
        print("STARTING SCRAPING")
        print("=" * 60)

        # Initialize scraper and use case
        scraper = AthleScraper()
        use_case = ScrapeRankingsUseCase(
            epreuve_repository=SQLAlchemyEpreuveRepository(session),
            ranking_repository=None,  # Will be imported from repositories
            scraper=scraper
        )

        # Import all repositories
        from src.infrastructure.database.repositories import (
            SQLAlchemyRankingRepository,
            SQLAlchemyAlertRepository,
        )

        use_case = ScrapeRankingsUseCase(
            epreuve_repository=SQLAlchemyEpreuveRepository(session),
            ranking_repository=SQLAlchemyRankingRepository(session),
            alert_repository=SQLAlchemyAlertRepository(session),
            scraper=scraper
        )

        # Run scraping
        result = use_case.execute(epreuve_id)

        print("\n" + "=" * 60)
        print("SCRAPING COMPLETED")
        print("=" * 60)
        print(f"[OK] Successfully scraped {result['rankings_count']} rankings")
        print(f"[OK] Detected {result['alerts_count']} ranking changes")
        print("=" * 60)

        return result

    except Exception as e:
        print(f"\n[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("ATHLE TRACKER - DATA INITIALIZATION")
    print("=" * 60)
    print()

    # Step 1: Create epreuve
    print("Step 1: Creating sample competition...")
    epreuve_id = create_sample_epreuve()
    print()

    # Step 2: Run scraping
    print("Step 2: Running scraping to populate data...")
    try:
        result = run_scraping(epreuve_id)
        print()
        print("[SUCCESS] Data initialization completed!")
        print()
        print("You can now:")
        print("- View rankings at: http://localhost:3000/rankings")
        print("- Check alerts at: http://localhost:3000/alerts")
        print("- Manage the competition in admin panel")
    except Exception as e:
        print()
        print("[FAILED] Data initialization encountered errors.")
        print("Please check the error messages above.")
        sys.exit(1)

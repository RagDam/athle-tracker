"""Use case for scraping rankings and generating alerts."""

import time
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from src.infrastructure.database.repositories import (
    SQLAlchemyAlertRepository,
    SQLAlchemyAthleteRepository,
    SQLAlchemyEpreuveRepository,
    SQLAlchemyFavoriteRepository,
    SQLAlchemyRankingRepository,
    SQLAlchemyScrapeLogRepository,
    SQLAlchemyUserRepository,
)
from src.infrastructure.scraper import AthleScraper, ScrapingError
from src.utils import logger


class ScrapeRankingsUseCase:
    """
    Use case for scraping rankings, storing them, and generating alerts.

    This orchestrates the entire workflow:
    1. Scrape rankings from athle.fr
    2. Store athletes and rankings in database
    3. Compare with previous rankings
    4. Generate alerts for significant changes
    5. Log the scraping operation
    """

    def __init__(self, session: Session) -> None:
        """Initialize use case with database session."""
        self.session = session
        self.scraper = AthleScraper()

        # Initialize repositories
        self.epreuve_repo = SQLAlchemyEpreuveRepository(session)
        self.athlete_repo = SQLAlchemyAthleteRepository(session)
        self.ranking_repo = SQLAlchemyRankingRepository(session)
        self.alert_repo = SQLAlchemyAlertRepository(session)
        self.favorite_repo = SQLAlchemyFavoriteRepository(session)
        self.scrape_log_repo = SQLAlchemyScrapeLogRepository(session)
        self.user_repo = SQLAlchemyUserRepository(session)

    async def execute(
        self,
        epreuve_code: int,
        sexe: str,
        annee: int = 2026,
        categorie: str = "CA",
    ) -> dict[str, Any]:
        """
        Execute the scraping workflow.

        Args:
            epreuve_code: Competition code (e.g., 670 for Javelin)
            sexe: Gender (M or F)
            annee: Year (default 2026)
            categorie: Category (default CA for Cadets)

        Returns:
            Dictionary with scraping results and statistics
        """
        start_time = time.time()
        snapshot_date = datetime.now()

        # Verify epreuve exists
        epreuve = self.epreuve_repo.get_by_code(epreuve_code)
        if not epreuve:
            logger.error(f"Epreuve with code {epreuve_code} not found")
            return {
                "success": False,
                "error": f"Epreuve {epreuve_code} not found",
            }

        try:
            # Step 1: Scrape rankings
            logger.info(f"Starting scrape for {epreuve.nom} ({sexe})")
            scraped_data = await self.scraper.scrape_rankings(
                epreuve_code, sexe, annee, categorie
            )

            if not scraped_data:
                logger.warning("No rankings data scraped")
                self._log_scrape(
                    epreuve_code, sexe, "partial", 0, time.time() - start_time, "No data found"
                )
                return {
                    "success": False,
                    "error": "No rankings data found",
                }

            # Step 2: Get previous rankings for comparison
            prev_date, prev_rankings = self.ranking_repo.get_latest_by_epreuve(
                epreuve_code, sexe
            )
            prev_ranks_map = {r.athlete_id: r.rank for r in prev_rankings} if prev_rankings else {}

            # Step 3: Process athletes and create rankings
            rankings_to_create = []
            alerts_to_create = []

            for data in scraped_data:
                # Get or create athlete
                athlete = self.athlete_repo.get_or_create(
                    {
                        "athlete_id": data["athlete_id"],
                        "name": data["name"],
                        "first_seen_date": snapshot_date,
                    }
                )

                # Create ranking entry
                ranking_data = {
                    "snapshot_date": snapshot_date,
                    "epreuve_code": epreuve_code,
                    "sexe": sexe,
                    "rank": data["rank"],
                    "athlete_id": data["athlete_id"],
                    "performance": data["performance"],
                    "performance_numeric": data["performance_numeric"],
                    "club": data.get("club"),
                    "ligue": data.get("ligue"),
                    "departement": data.get("departement"),
                }
                rankings_to_create.append(ranking_data)

                # Generate alerts if rank changed
                old_rank = prev_ranks_map.get(data["athlete_id"])
                new_rank = data["rank"]

                alert_data_list = self._check_alerts(
                    athlete.athlete_id,
                    athlete.name,
                    old_rank,
                    new_rank,
                    epreuve_code,
                    sexe,
                )
                alerts_to_create.extend(alert_data_list)

            # Step 4: Bulk insert rankings
            self.ranking_repo.create_bulk(rankings_to_create)
            logger.info(f"Created {len(rankings_to_create)} ranking entries")

            # Step 5: Create alerts
            if alerts_to_create:
                self.alert_repo.create_bulk(alerts_to_create)
                logger.info(f"Created {len(alerts_to_create)} alerts")

            # Step 6: Log success
            duration = time.time() - start_time
            self._log_scrape(
                epreuve_code, sexe, "success", len(scraped_data), duration, None
            )

            return {
                "success": True,
                "epreuve": epreuve.nom,
                "sexe": sexe,
                "rankings_count": len(scraped_data),
                "alerts_count": len(alerts_to_create),
                "duration_seconds": round(duration, 2),
                "snapshot_date": snapshot_date.isoformat(),
            }

        except ScrapingError as e:
            duration = time.time() - start_time
            error_msg = str(e)
            logger.error(f"Scraping failed: {error_msg}")
            self._log_scrape(epreuve_code, sexe, "error", 0, duration, error_msg)

            return {
                "success": False,
                "error": error_msg,
                "duration_seconds": round(duration, 2),
            }

        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            self._log_scrape(epreuve_code, sexe, "error", 0, duration, error_msg)

            return {
                "success": False,
                "error": error_msg,
                "duration_seconds": round(duration, 2),
            }

    def _check_alerts(
        self,
        athlete_id: str,
        athlete_name: str,
        old_rank: int | None,
        new_rank: int,
        epreuve_code: int,
        sexe: str,
    ) -> list[dict[str, Any]]:
        """
        Check if alerts should be generated for this ranking change.

        Alert types:
        - Top 3 (podium): critique
        - Top 10: important
        - Top 20: info
        - Favorites: info

        Args:
            athlete_id: Athlete ID
            athlete_name: Athlete name
            old_rank: Previous rank (None if new)
            new_rank: Current rank
            epreuve_code: Competition code
            sexe: Gender

        Returns:
            List of alert data dictionaries
        """
        alerts = []

        # Get all active users for alerts
        all_users = self.user_repo.list_all()
        active_users = [u for u in all_users if u.actif]

        # Check Top 3 (Podium) - CRITIQUE
        if new_rank <= 3:
            if old_rank is None or old_rank > 3:
                # Entered podium
                for user in active_users:
                    alerts.append(
                        {
                            "user_id": user.id,
                            "alert_type": "critique",
                            "athlete_id": athlete_id,
                            "epreuve_code": epreuve_code,
                            "sexe": sexe,
                            "title": f"🥇 Podium : {athlete_name}",
                            "message": f"{athlete_name} entre dans le Top 3 (rang {new_rank})",
                            "old_rank": old_rank,
                            "new_rank": new_rank,
                        }
                    )
        elif old_rank and old_rank <= 3:
            # Exited podium
            for user in active_users:
                alerts.append(
                    {
                        "user_id": user.id,
                        "alert_type": "critique",
                        "athlete_id": athlete_id,
                        "epreuve_code": epreuve_code,
                        "sexe": sexe,
                        "title": f"⚠️ Podium : {athlete_name}",
                        "message": f"{athlete_name} sort du Top 3 (rang {old_rank} → {new_rank})",
                        "old_rank": old_rank,
                        "new_rank": new_rank,
                    }
                )

        # Check Top 10 - IMPORTANT
        elif new_rank <= 10:
            if old_rank is None or old_rank > 10:
                # Entered Top 10
                for user in active_users:
                    alerts.append(
                        {
                            "user_id": user.id,
                            "alert_type": "important",
                            "athlete_id": athlete_id,
                            "epreuve_code": epreuve_code,
                            "sexe": sexe,
                            "title": f"⭐ Top 10 : {athlete_name}",
                            "message": f"{athlete_name} entre dans le Top 10 (rang {new_rank})",
                            "old_rank": old_rank,
                            "new_rank": new_rank,
                        }
                    )
        elif old_rank and old_rank <= 10:
            # Exited Top 10
            for user in active_users:
                alerts.append(
                    {
                        "user_id": user.id,
                        "alert_type": "important",
                        "athlete_id": athlete_id,
                        "epreuve_code": epreuve_code,
                        "sexe": sexe,
                        "title": f"📉 Top 10 : {athlete_name}",
                        "message": f"{athlete_name} sort du Top 10 (rang {old_rank} → {new_rank})",
                        "old_rank": old_rank,
                        "new_rank": new_rank,
                    }
                )

        # Check Top 20 - INFO
        elif new_rank <= 20:
            if old_rank is None or old_rank > 20:
                # Entered Top 20
                for user in active_users:
                    alerts.append(
                        {
                            "user_id": user.id,
                            "alert_type": "info",
                            "athlete_id": athlete_id,
                            "epreuve_code": epreuve_code,
                            "sexe": sexe,
                            "title": f"📊 Top 20 : {athlete_name}",
                            "message": f"{athlete_name} entre dans le Top 20 (rang {new_rank})",
                            "old_rank": old_rank,
                            "new_rank": new_rank,
                        }
                    )
        elif old_rank and old_rank <= 20:
            # Exited Top 20
            for user in active_users:
                alerts.append(
                    {
                        "user_id": user.id,
                        "alert_type": "info",
                        "athlete_id": athlete_id,
                        "epreuve_code": epreuve_code,
                        "sexe": sexe,
                        "title": f"📉 Top 20 : {athlete_name}",
                        "message": f"{athlete_name} sort du Top 20 (rang {old_rank} → {new_rank})",
                        "old_rank": old_rank,
                        "new_rank": new_rank,
                    }
                )

        # Check Favorites - INFO (for any rank change)
        if old_rank and old_rank != new_rank:
            # Get users who favorited this athlete
            for user in active_users:
                if self.favorite_repo.is_favorite(user.id, athlete_id, epreuve_code):
                    direction = "📈" if new_rank < old_rank else "📉"
                    alerts.append(
                        {
                            "user_id": user.id,
                            "alert_type": "info",
                            "athlete_id": athlete_id,
                            "epreuve_code": epreuve_code,
                            "sexe": sexe,
                            "title": f"{direction} Favori : {athlete_name}",
                            "message": f"{athlete_name} passe du rang {old_rank} au rang {new_rank}",
                            "old_rank": old_rank,
                            "new_rank": new_rank,
                        }
                    )

        return alerts

    def _log_scrape(
        self,
        epreuve_code: int,
        sexe: str,
        status: str,
        results_count: int,
        duration_seconds: float,
        error_message: str | None,
    ) -> None:
        """Log scraping operation."""
        self.scrape_log_repo.create(
            {
                "epreuve_code": epreuve_code,
                "sexe": sexe,
                "status": status,
                "results_count": results_count,
                "duration_seconds": duration_seconds,
                "error_message": error_message,
            }
        )

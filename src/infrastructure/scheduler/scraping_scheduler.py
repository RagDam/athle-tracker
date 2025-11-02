"""Scheduler for automatic daily scraping."""

import asyncio
import random
from datetime import datetime, time

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import settings
from src.core.use_cases import ScrapeRankingsUseCase
from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.database.repositories import SQLAlchemyEpreuveRepository
from src.utils import logger


class ScrapingScheduler:
    """
    Scheduler for automatic daily scraping of rankings.

    Features:
    - Random time within configured window (anti-detection)
    - Automatic scraping for all active events
    - Both male and female categories
    - Timezone aware (Europe/Paris)
    """

    def __init__(self) -> None:
        """Initialize scheduler with configuration."""
        self.scheduler = BackgroundScheduler(timezone=settings.timezone)
        self.timezone = pytz.timezone(settings.timezone)

    def _get_random_time_in_window(self) -> time:
        """
        Get random time within configured window.

        Returns:
            Random time object within start/end window
        """
        start_minutes = settings.scheduler_start_hour * 60 + settings.scheduler_start_minute
        end_minutes = settings.scheduler_end_hour * 60 + settings.scheduler_end_minute

        random_minutes = random.randint(start_minutes, end_minutes)
        hour = random_minutes // 60
        minute = random_minutes % 60

        return time(hour=hour, minute=minute)

    async def _scrape_all_active_events(self) -> None:
        """
        Scrape all active events (male and female).

        This is the main scheduled job that runs daily.
        """
        logger.info("=" * 60)
        logger.info("Starting scheduled scraping job")
        logger.info(f"Timestamp: {datetime.now(self.timezone)}")
        logger.info("=" * 60)

        session = SessionLocal()
        try:
            # Get all active events
            epreuve_repo = SQLAlchemyEpreuveRepository(session)
            active_events = epreuve_repo.list_active()

            if not active_events:
                logger.warning("No active events found for scraping")
                return

            logger.info(f"Found {len(active_events)} active event(s) to scrape")

            # Scrape each event (male only)
            for epreuve in active_events:
                try:
                    logger.info(f"Scraping {epreuve.nom} (Hommes)...")

                    # Create fresh session for each use case
                    scrape_session = SessionLocal()
                    use_case = ScrapeRankingsUseCase(scrape_session)

                    result = await use_case.execute(
                        epreuve_code=epreuve.code,
                        sexe="M",
                    )

                    if result["success"]:
                        logger.info(
                            f"✓ {epreuve.nom}: "
                            f"{result['rankings_count']} rankings, "
                            f"{result['alerts_count']} alerts, "
                            f"{result['duration_seconds']}s"
                        )
                    else:
                        logger.error(
                            f"✗ {epreuve.nom}: {result.get('error')}"
                        )

                    scrape_session.close()

                    # Small delay between events
                    await asyncio.sleep(random.uniform(3, 5))

                except Exception as e:
                    logger.error(
                        f"Error scraping {epreuve.nom}: {e}"
                    )
                    continue

            logger.info("=" * 60)
            logger.info("Scheduled scraping job completed")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Critical error in scheduled job: {e}")
        finally:
            session.close()

    def _scheduled_job(self) -> None:
        """Wrapper to run async scraping in event loop."""
        try:
            asyncio.run(self._scrape_all_active_events())
        except Exception as e:
            logger.error(f"Failed to run scheduled job: {e}")

    def start(self) -> None:
        """
        Start the scheduler.

        Schedules daily scraping at a random time within configured window.
        """
        if not settings.scheduler_enabled:
            logger.info("Scheduler is disabled in settings")
            return

        # Calculate next run time (random within window)
        next_run_time = self._get_random_time_in_window()

        logger.info(f"Scheduler starting with timezone: {settings.timezone}")
        logger.info(
            f"Scraping window: "
            f"{settings.scheduler_start_hour:02d}:{settings.scheduler_start_minute:02d} - "
            f"{settings.scheduler_end_hour:02d}:{settings.scheduler_end_minute:02d}"
        )
        logger.info(f"Next scheduled run: {next_run_time}")

        # Add daily job at random time
        # Note: We use cron trigger with hour/minute for daily execution
        self.scheduler.add_job(
            func=self._scheduled_job,
            trigger=CronTrigger(
                hour=next_run_time.hour,
                minute=next_run_time.minute,
                timezone=self.timezone,
            ),
            id="daily_scraping",
            name="Daily Rankings Scraping",
            replace_existing=True,
        )

        self.scheduler.start()
        logger.info("✓ Scheduler started successfully")

    def stop(self) -> None:
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")

    def run_manual_scrape(self, epreuve_code: int, sexe: str) -> dict:
        """
        Run manual scraping (for admin interface).

        Args:
            epreuve_code: Competition code
            sexe: Gender (M or F)

        Returns:
            Scraping result dictionary
        """
        logger.info(f"Running manual scrape: epreuve={epreuve_code}, sexe={sexe}")

        session = SessionLocal()
        try:
            use_case = ScrapeRankingsUseCase(session)
            result = asyncio.run(use_case.execute(epreuve_code, sexe))
            return result
        except Exception as e:
            logger.error(f"Manual scrape failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }
        finally:
            session.close()

    def get_next_run_time(self) -> str | None:
        """
        Get next scheduled run time.

        Returns:
            ISO format datetime string or None
        """
        job = self.scheduler.get_job("daily_scraping")
        if job and job.next_run_time:
            return job.next_run_time.isoformat()
        return None

"""Standalone script to run the scheduler."""

import signal
import sys
import time

from src.infrastructure.scheduler.scraping_scheduler import ScrapingScheduler
from src.utils import logger


def signal_handler(sig: int, frame: any) -> None:
    """Handle CTRL+C gracefully."""
    logger.info("Received shutdown signal, stopping scheduler...")
    scheduler.stop()
    sys.exit(0)


if __name__ == "__main__":
    logger.info("Starting Athle Tracker Scheduler")

    # Create and start scheduler
    scheduler = ScrapingScheduler()

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        scheduler.start()

        # Keep running
        logger.info("Scheduler is running. Press CTRL+C to stop.")
        while True:
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        scheduler.stop()
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        scheduler.stop()
        sys.exit(1)

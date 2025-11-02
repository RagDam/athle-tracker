"""Integration tests for ScrapeRankingsUseCase."""

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.orm import Session

from src.core.use_cases import ScrapeRankingsUseCase
from src.infrastructure.database.models import Epreuve, User


@pytest.mark.integration
class TestScrapeRankingsUseCase:
    """Integration tests for ScrapeRankingsUseCase."""

    @pytest.mark.asyncio
    async def test_execute_success_with_mocked_scraper(
        self,
        test_session: Session,
        test_epreuve: Epreuve,
        test_admin_user: User,
        sample_scrape_data,
    ) -> None:
        """Test successful scraping with mocked scraper."""
        use_case = ScrapeRankingsUseCase(test_session)

        # Mock the scraper to return sample data
        with patch.object(
            use_case.scraper, "scrape_rankings", new=AsyncMock(return_value=sample_scrape_data)
        ):
            result = await use_case.execute(epreuve_code=test_epreuve.code, sexe="M")

        assert result["success"] is True
        assert result["rankings_count"] == len(sample_scrape_data)
        assert "duration_seconds" in result

    @pytest.mark.asyncio
    async def test_execute_no_data(
        self, test_session: Session, test_epreuve: Epreuve
    ) -> None:
        """Test scraping when no data is returned."""
        use_case = ScrapeRankingsUseCase(test_session)

        # Mock scraper to return empty list
        with patch.object(use_case.scraper, "scrape_rankings", new=AsyncMock(return_value=[])):
            result = await use_case.execute(epreuve_code=test_epreuve.code, sexe="M")

        assert result["success"] is False
        assert "No rankings data found" in result["error"]

    @pytest.mark.asyncio
    async def test_execute_epreuve_not_found(self, test_session: Session) -> None:
        """Test scraping with nonexistent epreuve."""
        use_case = ScrapeRankingsUseCase(test_session)

        result = await use_case.execute(epreuve_code=9999, sexe="M")

        assert result["success"] is False
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_alerts_generation_top_3(
        self,
        test_session: Session,
        test_epreuve: Epreuve,
        test_admin_user: User,
        sample_scrape_data,
    ) -> None:
        """Test alert generation for Top 3 entries."""
        use_case = ScrapeRankingsUseCase(test_session)

        # Mock scraper
        with patch.object(
            use_case.scraper, "scrape_rankings", new=AsyncMock(return_value=sample_scrape_data)
        ):
            result = await use_case.execute(epreuve_code=test_epreuve.code, sexe="M")

        # Should generate alerts for Top 3 (all new athletes)
        assert result["alerts_count"] > 0

    @pytest.mark.asyncio
    async def test_check_alerts_new_athlete_top_3(
        self, test_session: Session, test_epreuve: Epreuve, test_admin_user: User
    ) -> None:
        """Test alert generation for new athlete in Top 3."""
        use_case = ScrapeRankingsUseCase(test_session)

        alerts = use_case._check_alerts(
            athlete_id="test_athlete",
            athlete_name="Test Athlete",
            old_rank=None,  # New athlete
            new_rank=1,
            epreuve_code=test_epreuve.code,
            sexe="M",
        )

        # Should generate critique alert for all users
        assert len(alerts) > 0
        assert all(a["alert_type"] == "critique" for a in alerts)
        assert all("Top 3" in a["title"] for a in alerts)

    @pytest.mark.asyncio
    async def test_check_alerts_exit_podium(
        self, test_session: Session, test_epreuve: Epreuve, test_admin_user: User
    ) -> None:
        """Test alert generation for exiting podium."""
        use_case = ScrapeRankingsUseCase(test_session)

        alerts = use_case._check_alerts(
            athlete_id="test_athlete",
            athlete_name="Test Athlete",
            old_rank=3,  # Was in Top 3
            new_rank=5,  # Now outside Top 3
            epreuve_code=test_epreuve.code,
            sexe="M",
        )

        assert len(alerts) > 0
        assert all(a["alert_type"] == "critique" for a in alerts)
        assert all("sort du Top 3" in a["message"] for a in alerts)

    @pytest.mark.asyncio
    async def test_check_alerts_top_10(
        self, test_session: Session, test_epreuve: Epreuve, test_admin_user: User
    ) -> None:
        """Test alert generation for Top 10 entry."""
        use_case = ScrapeRankingsUseCase(test_session)

        alerts = use_case._check_alerts(
            athlete_id="test_athlete",
            athlete_name="Test Athlete",
            old_rank=15,
            new_rank=8,  # Entered Top 10
            epreuve_code=test_epreuve.code,
            sexe="M",
        )

        assert len(alerts) > 0
        assert all(a["alert_type"] == "important" for a in alerts)
        assert all("Top 10" in a["title"] for a in alerts)

    @pytest.mark.asyncio
    async def test_check_alerts_top_20(
        self, test_session: Session, test_epreuve: Epreuve, test_admin_user: User
    ) -> None:
        """Test alert generation for Top 20 entry."""
        use_case = ScrapeRankingsUseCase(test_session)

        alerts = use_case._check_alerts(
            athlete_id="test_athlete",
            athlete_name="Test Athlete",
            old_rank=25,
            new_rank=18,  # Entered Top 20
            epreuve_code=test_epreuve.code,
            sexe="M",
        )

        assert len(alerts) > 0
        assert all(a["alert_type"] == "info" for a in alerts)
        assert all("Top 20" in a["title"] for a in alerts)

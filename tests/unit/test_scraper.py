"""Unit tests for AthleScraper."""

import pytest
from datetime import datetime

from src.infrastructure.scraper.athle_scraper import AthleScraper


@pytest.mark.unit
class TestAthleScraper:
    """Test cases for AthleScraper."""

    def test_build_url(self) -> None:
        """Test URL building."""
        scraper = AthleScraper()

        url = scraper._build_url(
            epreuve_code=670, sexe="M", annee=2026, categorie="CA"
        )

        assert "athle.fr" in url
        assert "frmepreuve=670" in url
        assert "frmsexe=M" in url
        assert "frmannee=2026" in url
        assert "frmcategorie=CA" in url

    def test_parse_performance_standard(self) -> None:
        """Test parsing standard performance."""
        scraper = AthleScraper()

        clean, numeric = scraper._parse_performance("58m14")

        assert clean == "58m14"
        assert numeric == 58.14

    def test_parse_performance_with_rp(self) -> None:
        """Test parsing performance with (RP) marker."""
        scraper = AthleScraper()

        clean, numeric = scraper._parse_performance("58m14 (RP)")

        assert clean == "58m14"
        assert numeric == 58.14

    def test_parse_performance_various_formats(self) -> None:
        """Test parsing various performance formats."""
        scraper = AthleScraper()

        test_cases = [
            ("49m29", "49m29", 49.29),
            ("47m20 (RP)", "47m20", 47.20),
            ("46m91 (RP)", "46m91", 46.91),
            ("46m19", "46m19", 46.19),
        ]

        for input_val, expected_clean, expected_numeric in test_cases:
            clean, numeric = scraper._parse_performance(input_val)
            assert clean == expected_clean
            assert numeric == expected_numeric

    def test_parse_ranking_row_mock(self) -> None:
        """Test parsing ranking row with mock data."""
        scraper = AthleScraper()

        # This is a simplified test - full test would require BeautifulSoup mocking
        # Just verify the method exists and doesn't crash with None
        result = scraper._parse_ranking_row(None)

        assert result is None

"""Scraper for athle.fr rankings with anti-detection."""

import asyncio
import random
import re
from datetime import datetime
from typing import Any, Optional

import httpx
from bs4 import BeautifulSoup

from src.config import settings
from src.infrastructure.scraper.user_agents import get_default_headers
from src.utils import logger


class ScrapingError(Exception):
    """Custom exception for scraping errors."""

    pass


class AthleScraper:
    """Scraper for athle.fr rankings with retry logic and anti-detection."""

    def __init__(self) -> None:
        """Initialize scraper with configuration."""
        self.base_url = settings.athle_base_url
        self.timeout = settings.scraping_timeout
        self.max_retries = settings.scraping_max_retries
        self.min_delay = settings.scraping_min_delay
        self.max_delay = settings.scraping_max_delay

    async def _random_delay(self) -> None:
        """Add random delay to avoid detection."""
        delay = random.uniform(self.min_delay, self.max_delay)
        await asyncio.sleep(delay)

    def _build_url(
        self,
        epreuve_code: int,
        sexe: str,
        annee: int = 2026,
        categorie: str = "CA",
    ) -> str:
        """
        Build athle.fr URL for rankings.

        Args:
            epreuve_code: Competition code (e.g., 670 for Javelin)
            sexe: Gender (M or F)
            annee: Year (default 2026)
            categorie: Category (default CA for Cadets)

        Returns:
            Complete URL for scraping
        """
        params = {
            "frmpostback": "true",
            "frmbase": "bilans",
            "frmmode": "1",
            "frmespace": "0",
            "frmannee": str(annee),
            "frmepreuve": str(epreuve_code),
            "frmsexe": sexe,
            "frmcategorie": categorie,
            "frmdepartement": "",
            "frmligue": "",
            "frmnationalite": "",
            "frmvent": "VR",
            "frmamaxi": "",
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.base_url}?{query_string}"

    def _parse_performance(self, performance_str: str) -> tuple[str, float]:
        """
        Parse performance string to extract clean value and numeric representation.

        Args:
            performance_str: Performance string (e.g., "58m14 (RP)", "49m29")

        Returns:
            Tuple of (clean_performance, numeric_value)

        Examples:
            "58m14 (RP)" -> ("58m14", 58.14)
            "49m29" -> ("49m29", 49.29)
            "47m20 (RP)" -> ("47m20", 47.20)
        """
        # Remove (RP) and other markers
        clean = re.sub(r"\s*\([^)]*\)", "", performance_str).strip()

        # Extract numeric value (e.g., "58m14" -> 58.14)
        match = re.match(r"(\d+)m(\d+)", clean)
        if match:
            meters = int(match.group(1))
            centimeters = int(match.group(2))
            numeric_value = meters + (centimeters / 100.0)
            return clean, numeric_value

        # Fallback: try to extract any number
        numbers = re.findall(r"\d+\.?\d*", clean)
        if numbers:
            numeric_value = float(numbers[0])
            return clean, numeric_value

        # If no pattern matches, return 0.0
        logger.warning(f"Could not parse performance: {performance_str}")
        return clean, 0.0

    def _parse_ranking_row(self, row: Any, last_valid_rank: int) -> Optional[tuple[dict[str, Any], int]]:
        """
        Parse a single ranking row from HTML table.

        Args:
            row: BeautifulSoup table row element
            last_valid_rank: Last valid rank seen (for ex-aequo handling)

        Returns:
            Tuple of (ranking data dict, updated last_valid_rank) or None if parsing fails
        """
        try:
            cells = row.find_all("td")
            # Need at least rank, perf, name + some metadata (relaxed from 8 to 3+)
            if len(cells) < 3:
                return None

            # Extract data from cells
            rank_text = cells[0].get_text(strip=True)
            performance_text = cells[1].get_text(strip=True)
            name = cells[2].get_text(strip=True)
            club = cells[3].get_text(strip=True) if len(cells) > 3 else None
            ligue = cells[4].get_text(strip=True) if len(cells) > 4 else None
            departement = cells[5].get_text(strip=True) if len(cells) > 5 else None
            infos = cells[6].get_text(strip=True) if len(cells) > 6 else None
            date_text = cells[7].get_text(strip=True) if len(cells) > 7 else ""
            lieu = cells[8].get_text(strip=True) if len(cells) > 8 else None

            # Skip rows without valid data (detail rows, empty rows)
            if not name or not performance_text:
                return None

            # Parse rank (handle tied ranks like "3", "3=", or "-" for ex-aequo)
            if rank_text == "-":
                # Ex-aequo: use last valid rank (passed as parameter)
                rank = last_valid_rank
                new_last_valid_rank = last_valid_rank  # Don't update
            else:
                rank_digits = re.sub(r"[^0-9]", "", rank_text)
                if not rank_digits:
                    return None
                rank = int(rank_digits)
                new_last_valid_rank = rank  # Update for next row

            # Parse performance - MUST contain 'm' or digits to be valid
            # This filters out detail rows where perf_text is actually a club name
            if not re.search(r'\d+m\d+|\d+\.\d+', performance_text, re.IGNORECASE):
                return None

            performance, performance_numeric = self._parse_performance(performance_text)

            # Parse date (DD/MM/YY format)
            if date_text:
                try:
                    date_obj = datetime.strptime(date_text, "%d/%m/%y")
                except ValueError:
                    date_obj = datetime.now()
            else:
                date_obj = datetime.now()

            # Generate athlete_id from name (normalized)
            athlete_id = re.sub(r"[^a-zA-Z0-9]", "_", name.lower())

            ranking_data = {
                "rank": rank,
                "athlete_id": athlete_id,
                "name": name,
                "performance": performance,
                "performance_numeric": performance_numeric,
                "club": club,
                "ligue": ligue,
                "departement": departement,
                "infos": infos,
                "date": date_obj,
                "lieu": lieu,
            }

            return (ranking_data, new_last_valid_rank)

        except Exception as e:
            logger.warning(f"Failed to parse ranking row: {e}")
            return None

    async def scrape_rankings(
        self,
        epreuve_code: int,
        sexe: str,
        annee: int = 2026,
        categorie: str = "CA",
    ) -> list[dict[str, Any]]:
        """
        Scrape rankings from athle.fr with retry logic.

        Args:
            epreuve_code: Competition code (e.g., 670 for Javelin)
            sexe: Gender (M or F)
            annee: Year (default 2026)
            categorie: Category (default CA for Cadets)

        Returns:
            List of ranking dictionaries

        Raises:
            ScrapingError: If scraping fails after all retries
        """
        url = self._build_url(epreuve_code, sexe, annee, categorie)
        logger.info(f"Scraping rankings: epreuve={epreuve_code}, sexe={sexe}")

        for attempt in range(1, self.max_retries + 1):
            try:
                # Random delay before request (except first attempt)
                if attempt > 1:
                    await self._random_delay()

                # Make request with random user agent
                headers = get_default_headers()
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    logger.debug(f"Attempt {attempt}/{self.max_retries}: GET {url}")
                    response = await client.get(url, headers=headers, follow_redirects=True)
                    response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.text, "lxml")

                # Find results table (new structure with id="ctnBilans")
                table = soup.find("table", id="ctnBilans")
                if not table:
                    logger.warning("No results table found with id=ctnBilans")
                    # Debug: check what tables exist
                    all_tables = soup.find_all("table")
                    logger.warning(f"Found {len(all_tables)} tables total")
                    for i, tbl in enumerate(all_tables[:5]):  # Log first 5 tables
                        logger.warning(f"  Table {i+1}: classes={tbl.get('class')}, id={tbl.get('id')}")

                    # Try fallback: look for reveal-table class
                    table = soup.find("table", class_="reveal-table")
                    if table:
                        logger.info("Found table with class=reveal-table, using fallback")
                    else:
                        logger.error("No suitable table found")
                        return []

                # Parse rows - skip first 3 rows (headers/info), row 3 is column names
                all_rows = table.find_all("tr")
                data_rows = all_rows[4:] if len(all_rows) > 4 else []  # Data starts at row 4
                rankings = []

                # Track last valid rank for ex-aequo handling
                last_valid_rank = 0

                for row in data_rows:
                    parsed_result = self._parse_ranking_row(row, last_valid_rank)
                    if parsed_result:
                        ranking_data, last_valid_rank = parsed_result
                        rankings.append(ranking_data)

                logger.info(f"Successfully scraped {len(rankings)} rankings")
                return rankings

            except httpx.HTTPStatusError as e:
                logger.warning(
                    f"HTTP error on attempt {attempt}/{self.max_retries}: {e.response.status_code}"
                )
                if attempt == self.max_retries:
                    raise ScrapingError(
                        f"HTTP error after {self.max_retries} attempts: {e.response.status_code}"
                    ) from e

            except httpx.TimeoutException as e:
                logger.warning(f"Timeout on attempt {attempt}/{self.max_retries}")
                if attempt == self.max_retries:
                    raise ScrapingError(
                        f"Timeout after {self.max_retries} attempts"
                    ) from e

            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt}/{self.max_retries}: {e}")
                if attempt == self.max_retries:
                    raise ScrapingError(
                        f"Scraping failed after {self.max_retries} attempts: {str(e)}"
                    ) from e

            # Exponential backoff before retry
            if attempt < self.max_retries:
                backoff_delay = 2**attempt
                logger.info(f"Retrying in {backoff_delay} seconds...")
                await asyncio.sleep(backoff_delay)

        # Should never reach here, but just in case
        raise ScrapingError("Scraping failed: Max retries exceeded")

"""
Test script for all API endpoints.
Tests authentication, rankings, alerts, epreuves, users, and scraping endpoints.
"""

import sys
from pathlib import Path
import requests
from typing import Optional

# Configuration
API_BASE_URL = "http://localhost:8000/api"
ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = "admin123"
USER_EMAIL = "user@test.com"
USER_PASSWORD = "user123"


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    """Test all API endpoints."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.admin_token: Optional[str] = None
        self.user_token: Optional[str] = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "total": 0,
        }

    def print_header(self, text: str):
        """Print section header."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

    def print_test(self, test_name: str, passed: bool, details: str = ""):
        """Print test result."""
        self.test_results["total"] += 1
        if passed:
            self.test_results["passed"] += 1
            status = f"{Colors.GREEN}[OK]{Colors.RESET}"
        else:
            self.test_results["failed"] += 1
            status = f"{Colors.RED}[FAIL]{Colors.RESET}"

        print(f"{status} {test_name}")
        if details:
            print(f"     {Colors.YELLOW}{details}{Colors.RESET}")

    def test_health(self):
        """Test health check endpoint."""
        self.print_header("1. HEALTH CHECK")

        try:
            response = requests.get(f"{self.base_url}/health")
            passed = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.json()}"
            self.print_test("GET /health", passed, details)
        except Exception as e:
            self.print_test("GET /health", False, f"Error: {e}")

    def test_auth(self):
        """Test authentication endpoints."""
        self.print_header("2. AUTHENTICATION")

        # Test admin login
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                self.admin_token = data.get("access_token")
                details = f"Token received: {self.admin_token[:20]}... Role: {data['user']['role']}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"

            self.print_test("POST /auth/login (admin)", passed, details)
        except Exception as e:
            self.print_test("POST /auth/login (admin)", False, f"Error: {e}")

        # Test user login
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": USER_EMAIL, "password": USER_PASSWORD}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                self.user_token = data.get("access_token")
                details = f"Token received: {self.user_token[:20]}... Role: {data['user']['role']}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"

            self.print_test("POST /auth/login (user)", passed, details)
        except Exception as e:
            self.print_test("POST /auth/login (user)", False, f"Error: {e}")

        # Test invalid login
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": "invalid@test.com", "password": "wrongpassword"}
            )
            passed = response.status_code == 401
            details = f"Status: {response.status_code} (should be 401)"
            self.print_test("POST /auth/login (invalid credentials)", passed, details)
        except Exception as e:
            self.print_test("POST /auth/login (invalid credentials)", False, f"Error: {e}")

    def test_rankings(self):
        """Test rankings endpoints."""
        self.print_header("3. RANKINGS")

        if not self.user_token:
            print(f"{Colors.YELLOW}Skipping rankings tests (no user token){Colors.RESET}")
            return

        headers = {"Authorization": f"Bearer {self.user_token}"}

        # Test GET /rankings/all
        try:
            response = requests.get(f"{self.base_url}/rankings/all", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Rankings count: {len(data)}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"

            self.print_test("GET /rankings/all", passed, details)
        except Exception as e:
            self.print_test("GET /rankings/all", False, f"Error: {e}")

        # Test GET /rankings/ with params
        try:
            response = requests.get(
                f"{self.base_url}/rankings/",
                headers=headers,
                params={"epreuve_code": 1, "sexe": "M"}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Rankings count: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /rankings/ (with epreuve_code)", passed, details)
        except Exception as e:
            self.print_test("GET /rankings/ (with epreuve_code)", False, f"Error: {e}")

        # Test GET /rankings/podium
        try:
            response = requests.get(
                f"{self.base_url}/rankings/podium",
                headers=headers,
                params={"epreuve_code": 1, "sexe": "M", "limit": 3}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Podium size: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /rankings/podium", passed, details)
        except Exception as e:
            self.print_test("GET /rankings/podium", False, f"Error: {e}")

    def test_alerts(self):
        """Test alerts endpoints."""
        self.print_header("4. ALERTS")

        if not self.user_token:
            print(f"{Colors.YELLOW}Skipping alerts tests (no user token){Colors.RESET}")
            return

        headers = {"Authorization": f"Bearer {self.user_token}"}

        # Test GET /alerts/
        try:
            response = requests.get(f"{self.base_url}/alerts/", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Alerts count: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /alerts/", passed, details)
        except Exception as e:
            self.print_test("GET /alerts/", False, f"Error: {e}")

        # Test GET /alerts/unread-count
        try:
            response = requests.get(f"{self.base_url}/alerts/unread-count", headers=headers)
            passed = response.status_code == 200
            if passed:
                count = response.json()
                details = f"Unread count: {count}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /alerts/unread-count", passed, details)
        except Exception as e:
            self.print_test("GET /alerts/unread-count", False, f"Error: {e}")

    def test_epreuves(self):
        """Test epreuves endpoints."""
        self.print_header("5. ÉPREUVES")

        if not self.admin_token:
            print(f"{Colors.YELLOW}Skipping epreuves tests (no admin token){Colors.RESET}")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test GET /epreuves/
        try:
            response = requests.get(f"{self.base_url}/epreuves/", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Épreuves count: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /epreuves/", passed, details)
        except Exception as e:
            self.print_test("GET /epreuves/", False, f"Error: {e}")

        # Test GET /epreuves/active
        try:
            response = requests.get(f"{self.base_url}/epreuves/active", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Active épreuves: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /epreuves/active", passed, details)
        except Exception as e:
            self.print_test("GET /epreuves/active", False, f"Error: {e}")

        # Test GET /epreuves/{id}
        try:
            response = requests.get(f"{self.base_url}/epreuves/1", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Épreuve: {data.get('nom', 'N/A')}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /epreuves/1", passed, details)
        except Exception as e:
            self.print_test("GET /epreuves/1", False, f"Error: {e}")

    def test_users(self):
        """Test users endpoints."""
        self.print_header("6. USERS (Admin only)")

        if not self.admin_token:
            print(f"{Colors.YELLOW}Skipping users tests (no admin token){Colors.RESET}")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test GET /users/
        try:
            response = requests.get(f"{self.base_url}/users/", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Users count: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /users/", passed, details)
        except Exception as e:
            self.print_test("GET /users/", False, f"Error: {e}")

        # Test unauthorized access (user trying to access admin endpoint)
        if self.user_token:
            user_headers = {"Authorization": f"Bearer {self.user_token}"}
            try:
                response = requests.get(f"{self.base_url}/users/", headers=user_headers)
                passed = response.status_code == 403
                details = f"Status: {response.status_code} (should be 403 Forbidden)"
                self.print_test("GET /users/ (unauthorized user)", passed, details)
            except Exception as e:
                self.print_test("GET /users/ (unauthorized user)", False, f"Error: {e}")

    def test_scraping(self):
        """Test scraping endpoints."""
        self.print_header("7. SCRAPING (Admin only)")

        if not self.admin_token:
            print(f"{Colors.YELLOW}Skipping scraping tests (no admin token){Colors.RESET}")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test GET /scraping/scheduler/status
        try:
            response = requests.get(f"{self.base_url}/scraping/scheduler/status", headers=headers)
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Scheduler enabled: {data.get('enabled', 'N/A')}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /scraping/scheduler/status", passed, details)
        except Exception as e:
            self.print_test("GET /scraping/scheduler/status", False, f"Error: {e}")

        # Test GET /scraping/logs
        try:
            response = requests.get(
                f"{self.base_url}/scraping/logs",
                headers=headers,
                params={"limit": 10}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                details = f"Logs count: {len(data)}"
            else:
                details = f"Status: {response.status_code}"

            self.print_test("GET /scraping/logs", passed, details)
        except Exception as e:
            self.print_test("GET /scraping/logs", False, f"Error: {e}")

    def print_summary(self):
        """Print test summary."""
        self.print_header("TEST SUMMARY")

        total = self.test_results["total"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"Total tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
        print(f"Success rate: {success_rate:.1f}%\n")

        if failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}Some tests failed. Please check the output above.{Colors.RESET}")

    def run_all_tests(self):
        """Run all endpoint tests."""
        print(f"{Colors.BOLD}")
        print("=" * 60)
        print("ATHLE TRACKER - API ENDPOINT TESTS")
        print("=" * 60)
        print(f"{Colors.RESET}")
        print(f"API Base URL: {self.base_url}\n")

        self.test_health()
        self.test_auth()
        self.test_rankings()
        self.test_alerts()
        self.test_epreuves()
        self.test_users()
        self.test_scraping()
        self.print_summary()


if __name__ == "__main__":
    tester = APITester(API_BASE_URL)
    tester.run_all_tests()

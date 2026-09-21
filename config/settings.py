"""Single source of truth for runtime configuration."""

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    environment: str
    base_url: str
    api_base_url: str
    test_user_email: str
    test_user_password: str
    admin_email: str
    admin_password: str
    team_user_email: str
    team_user_password: str
    client_user_email: str
    client_user_password: str
    other_owner_email: str
    other_owner_password: str
    headless: bool
    default_timeout_ms: int
    navigation_timeout_ms: int
    test_run_id: str
    allow_destructive_tests: bool
    allow_production_tests: bool
    fail_on_browser_errors: bool
    browser_error_allowlist: tuple[str, ...]

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            environment=os.getenv("TEST_ENVIRONMENT", "local").strip().lower(),
            base_url=os.getenv("BASE_URL", "http://localhost:5275").rstrip("/"),
            api_base_url=os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/"),
            test_user_email=os.getenv("TEST_USER_EMAIL", ""),
            test_user_password=os.getenv("TEST_USER_PASSWORD", ""),
            admin_email=os.getenv("ADMIN_EMAIL", ""),
            admin_password=os.getenv("ADMIN_PASSWORD", ""),
            team_user_email=os.getenv("TEAM_USER_EMAIL", ""),
            team_user_password=os.getenv("TEAM_USER_PASSWORD", ""),
            client_user_email=os.getenv("CLIENT_USER_EMAIL", ""),
            client_user_password=os.getenv("CLIENT_USER_PASSWORD", ""),
            other_owner_email=os.getenv("OTHER_OWNER_EMAIL", ""),
            other_owner_password=os.getenv("OTHER_OWNER_PASSWORD", ""),
            headless=os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"},
            default_timeout_ms=int(os.getenv("DEFAULT_TIMEOUT_MS", "10000")),
            navigation_timeout_ms=int(os.getenv("NAVIGATION_TIMEOUT_MS", "20000")),
            test_run_id=os.getenv("TEST_RUN_ID", "local"),
            allow_destructive_tests=_as_bool("ALLOW_DESTRUCTIVE_TESTS", False),
            allow_production_tests=_as_bool("ALLOW_PRODUCTION_TESTS", False),
            fail_on_browser_errors=_as_bool("FAIL_ON_BROWSER_ERRORS", True),
            browser_error_allowlist=tuple(
                item.strip()
                for item in os.getenv("BROWSER_ERROR_ALLOWLIST", "").split(",")
                if item.strip()
            ),
        )

    def validate(self) -> None:
        """Reject malformed and unsafe environment configuration."""
        for name, value in (("BASE_URL", self.base_url), ("API_BASE_URL", self.api_base_url)):
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError(f"{name} must be an absolute http(s) URL: {value!r}")
        production_hint = self.environment in {"prod", "production"} or any(
            token in urlparse(url).netloc.lower()
            for url in (self.base_url, self.api_base_url)
            for token in ("prod.", "production.")
        )
        if production_hint and not self.allow_production_tests:
            raise ValueError(
                "Production-like target blocked. Use staging, or explicitly set "
                "ALLOW_PRODUCTION_TESTS=true for authorized read-only checks."
            )

    def require_role(self, role: str) -> tuple[str, str]:
        credentials = {
            "owner": (self.test_user_email, self.test_user_password),
            "admin": (self.admin_email, self.admin_password),
            "team": (self.team_user_email, self.team_user_password),
            "client": (self.client_user_email, self.client_user_password),
            "other_owner": (self.other_owner_email, self.other_owner_password),
        }
        email, password = credentials[role]
        if not email or not password:
            raise ValueError(f"Missing {role} test credentials in the environment")
        return email, password


def _as_bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes"}

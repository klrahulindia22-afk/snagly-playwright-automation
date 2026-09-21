"""Single source of truth for runtime configuration."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
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

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
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
        )

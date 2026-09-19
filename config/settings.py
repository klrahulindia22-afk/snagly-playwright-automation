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
    headless: bool

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            base_url=os.getenv("BASE_URL", "http://localhost:5275").rstrip("/"),
            api_base_url=os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/"),
            test_user_email=os.getenv("TEST_USER_EMAIL", ""),
            test_user_password=os.getenv("TEST_USER_PASSWORD", ""),
            admin_email=os.getenv("ADMIN_EMAIL", ""),
            admin_password=os.getenv("ADMIN_PASSWORD", ""),
            headless=os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"},
        )

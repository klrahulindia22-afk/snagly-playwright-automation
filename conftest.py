import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        base_url=os.getenv("BASE_URL", "http://localhost:5275").rstrip("/"),
        email=os.getenv("TEST_USER_EMAIL", ""),
        password=os.getenv("TEST_USER_PASSWORD", ""),
    )


@pytest.fixture
def app_url(settings: Settings) -> str:
    return settings.base_url


@pytest.fixture
def authenticated_page(page, settings: Settings):
    if not settings.email or not settings.password:
        pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD in .env to run authenticated tests.")

    from pages.login_page import LoginPage

    login = LoginPage(page, settings.base_url)
    login.open()
    login.login(settings.email, settings.password)
    login.expect_authenticated()
    return page

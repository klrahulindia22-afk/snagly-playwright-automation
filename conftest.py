import pytest

from config.settings import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_environment()


@pytest.fixture
def app_url(settings: Settings) -> str:
    return settings.base_url


@pytest.fixture(scope="session")
def browser_type_launch_args(settings: Settings):
    """Use .env defaults while still allowing --headed to override for debugging."""
    return {"headless": settings.headless}


@pytest.fixture
def authenticated_page(page, settings: Settings):
    if not settings.test_user_email or not settings.test_user_password:
        pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD in .env to run authenticated tests.")

    from pages.login_page import LoginPage

    login = LoginPage(page, settings.base_url)
    login.open()
    login.login(settings.test_user_email, settings.test_user_password)
    login.expect_authenticated()
    return page


@pytest.fixture(autouse=True)
def standardise_browser(page):
    """Give every UI check stable timing and evidence-friendly browser defaults."""
    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(20_000)
    yield page


@pytest.fixture
def api_client(playwright, settings: Settings):
    """Fresh API context per test prevents cookies and headers leaking between tests."""
    context = playwright.request.new_context(base_url=settings.api_base_url)
    yield context
    context.dispose()

from collections.abc import Callable

import pytest
from playwright.sync_api import Browser, Page

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


def _credentials(settings: Settings, role: str) -> tuple[str, str]:
    mapping = {
        "owner": (settings.test_user_email, settings.test_user_password),
        "admin": (settings.admin_email, settings.admin_password),
        "team": (settings.team_user_email, settings.team_user_password),
        "client": (settings.client_user_email, settings.client_user_password),
        "other_owner": (settings.other_owner_email, settings.other_owner_password),
    }
    return mapping[role]


@pytest.fixture
def page_as(browser: Browser, settings: Settings) -> Callable[[str], Page]:
    """Create isolated authenticated pages for RBAC and concurrency tests."""
    contexts = []

    def factory(role: str) -> Page:
        email, password = _credentials(settings, role)
        if not email or not password:
            pytest.skip(f"Set {role.upper()} credentials in .env to run this test.")
        context = browser.new_context(base_url=settings.base_url)
        contexts.append(context)
        role_page = context.new_page()
        from pages.login_page import LoginPage
        login = LoginPage(role_page, settings.base_url)
        login.open()
        login.login(email, password)
        login.expect_authenticated()
        return role_page

    yield factory
    for context in contexts:
        context.close()


@pytest.fixture(autouse=True)
def standardise_browser(request, settings: Settings):
    """Give every UI check stable timing and evidence-friendly browser defaults."""
    if "page" not in request.fixturenames:
        yield
        return
    page = request.getfixturevalue("page")
    page.set_default_timeout(settings.default_timeout_ms)
    page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    yield page


@pytest.fixture
def api_client(playwright, settings: Settings):
    """Fresh API context per test prevents cookies and headers leaking between tests."""
    context = playwright.request.new_context(base_url=settings.api_base_url)
    yield context
    context.dispose()


@pytest.fixture
def authenticated_api(api_client, settings: Settings):
    if not settings.test_user_email or not settings.test_user_password:
        pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD to run authenticated API tests.")
    from clients.snagly_api import SnaglyApi
    client = SnaglyApi(api_client)
    client.login(settings.test_user_email, settings.test_user_password)
    return client


@pytest.fixture
def disposable_board(authenticated_api, settings: Settings):
    from utils.contracts import assert_envelope
    from utils.data_factory import BoardData
    data = BoardData.build(settings.test_run_id)
    board = assert_envelope(authenticated_api.create_board(data.name, data.description), 201)
    yield board
    authenticated_api.delete_board(board["id"])


@pytest.fixture
def disposable_list(authenticated_api, disposable_board):
    from utils.contracts import assert_envelope
    created = assert_envelope(authenticated_api.create_list(disposable_board["id"], "E2E Backlog"), 201)
    return created


@pytest.fixture
def disposable_card(authenticated_api, disposable_board, disposable_list, settings: Settings):
    from utils.contracts import assert_envelope
    from utils.data_factory import unique_name
    card = assert_envelope(authenticated_api.create_card(disposable_board["id"], disposable_list["id"], unique_name("Card", settings.test_run_id)), 201)
    yield card
    authenticated_api.delete_card(card["id"])

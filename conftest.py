from collections.abc import Callable
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page

from config.settings import Settings
from test_data.registry import CaseData, TestDataRegistry
from utils.files import create_sized_file


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_environment()


@pytest.fixture(scope="session")
def test_data_registry() -> TestDataRegistry:
    """Load and validate the complete manual-case data catalogue once per run."""
    return TestDataRegistry()


@pytest.fixture
def case_data(request, test_data_registry: TestDataRegistry, settings: Settings, tmp_path: Path) -> CaseData:
    """Resolve data automatically from the test's ``case_id`` marker."""
    marker = request.node.get_closest_marker("case_id")
    if marker is None or not marker.args:
        pytest.fail("The case_data fixture requires @pytest.mark.case_id('SNAG-TC-###')")
    return test_data_registry.for_case(str(marker.args[0]), settings, tmp_path)


@pytest.fixture
def case_user(case_data: CaseData) -> dict[str, str]:
    """Return credentials for the role assigned to the current manual case."""
    credentials = case_data.values["users"][case_data.role]
    if not credentials["email"] or not credentials["password"]:
        pytest.skip(f"Set {case_data.role.upper()} credentials in .env to run this test.")
    return credentials


@pytest.fixture
def test_file_factory(tmp_path: Path):
    """Create disposable attachment payloads without storing binaries in Git."""
    def factory(name: str, size_bytes: int, content: bytes = b"E2E") -> Path:
        return create_sized_file(tmp_path, name, size_bytes, content)

    return factory


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

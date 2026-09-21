import json
from collections.abc import Callable
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page

from config.settings import Settings
from test_data.registry import CaseData, TestDataRegistry
from utils.files import create_sized_file


@pytest.fixture(scope="session")
def settings() -> Settings:
    configured = Settings.from_environment()
    configured.validate()
    return configured


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
    if len(marker.args) != 1:
        pytest.fail("case_data requires exactly one case ID on the current test parameter")
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
    try:
        email, password = settings.require_role("owner")
    except ValueError as error:
        pytest.skip(str(error))

    from pages.login_page import LoginPage

    login = LoginPage(page, settings.base_url)
    login.open()
    login.login(email, password)
    login.expect_authenticated()
    return page


def _credentials(settings: Settings, role: str) -> tuple[str, str]:
    return settings.require_role(role)


@pytest.fixture
def page_as(browser: Browser, settings: Settings) -> Callable[[str], Page]:
    """Create isolated authenticated pages for RBAC and concurrency tests."""
    contexts = []

    def factory(role: str) -> Page:
        try:
            email, password = _credentials(settings, role)
        except ValueError as error:
            pytest.skip(str(error))
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
    browser_errors: list[str] = []

    def allowed(message: str) -> bool:
        return any(item in message for item in settings.browser_error_allowlist)

    page.on(
        "console",
        lambda message: browser_errors.append(f"console: {message.text}")
        if message.type == "error" and not allowed(message.text)
        else None,
    )
    page.on(
        "pageerror",
        lambda error: browser_errors.append(f"pageerror: {error}")
        if not allowed(str(error))
        else None,
    )
    page.set_default_timeout(settings.default_timeout_ms)
    page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    yield page
    if settings.fail_on_browser_errors and browser_errors:
        pytest.fail("Unexpected browser errors:\n" + "\n".join(browser_errors))


@pytest.fixture
def api_client(playwright, settings: Settings):
    """Fresh API context per test prevents cookies and headers leaking between tests."""
    context = playwright.request.new_context(base_url=settings.api_base_url)
    yield context
    context.dispose()


@pytest.fixture
def authenticated_api(api_client, settings: Settings):
    try:
        email, password = settings.require_role("owner")
    except ValueError as error:
        pytest.skip(str(error))
    from clients.snagly_api import SnaglyApi
    client = SnaglyApi(api_client)
    client.login(email, password)
    return client


@pytest.fixture
def disposable_board(authenticated_api, settings: Settings):
    from utils.contracts import assert_envelope
    from utils.data_factory import BoardData
    data = BoardData.build(settings.test_run_id)
    board = assert_envelope(authenticated_api.create_board(data.name, data.description), 201)
    yield board
    response = authenticated_api.delete_board(board["id"])
    if response.status not in {200, 204, 404}:
        pytest.fail(f"Board cleanup failed: {response.status} {response.text()}")


def pytest_addoption(parser):
    parser.addoption(
        "--traceability-output",
        action="store",
        default="",
        help="Write case-level traceability JSON and Markdown using this path prefix.",
    )


def pytest_collection_modifyitems(config, items):
    """Enforce case links and destructive-test authorization."""
    missing_case_ids = []
    unknown_case_ids = []
    valid_case_ids = set(TestDataRegistry().ids())
    allow_destructive = Settings.from_environment().allow_destructive_tests
    for item in items:
        marker = item.get_closest_marker("case_id")
        if "/tests/unit/" not in str(item.path).replace("\\", "/") and not marker:
            missing_case_ids.append(item.nodeid)
        if marker:
            unknown_case_ids.extend(
                f"{item.nodeid}: {case_id}"
                for case_id in marker.args
                if str(case_id) not in valid_case_ids
            )
        if item.get_closest_marker("destructive") and not allow_destructive:
            item.add_marker(pytest.mark.skip(reason="Set ALLOW_DESTRUCTIVE_TESTS=true to authorize this test"))
    if missing_case_ids:
        raise pytest.UsageError(
            "Application tests missing @pytest.mark.case_id: " + ", ".join(missing_case_ids)
        )
    if unknown_case_ids:
        raise pytest.UsageError("Unknown case IDs: " + ", ".join(unknown_case_ids))


def pytest_collection_finish(session):
    output = session.config.getoption("--traceability-output")
    if not output:
        return
    registry = TestDataRegistry()
    mappings: dict[str, list[str]] = {}
    for item in session.items:
        marker = item.get_closest_marker("case_id")
        if marker:
            for case_id in marker.args:
                mappings.setdefault(str(case_id), []).append(item.nodeid)
    rows = []
    for case_id in registry.ids():
        case = registry.raw(case_id)
        tests = mappings.get(case_id, [])
        rows.append({
            "case_id": case_id,
            "module": case["module"],
            "scenario": case["scenario"],
            "priority": case["priority"],
            "automation_status": "automated" if tests else "pending",
            "tests": tests,
        })
    prefix = Path(output)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    prefix.with_suffix(".json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Generated automation traceability",
        "",
        "| Case ID | Module | Priority | Status | Automated test |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        tests = "<br>".join(f"`{test}`" for test in row["tests"]) or "—"
        lines.append(
            f"| {row['case_id']} | {row['module']} | {row['priority']} | "
            f"{row['automation_status']} | {tests} |"
        )
    prefix.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


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

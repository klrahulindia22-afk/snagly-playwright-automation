# Snagly Playwright Automation Framework

Production-grade Python, Playwright and pytest automation for the Snagly bug-reporting and client-communication platform.

The framework validates the React/Vite web application and FastAPI backend through browser journeys, API contracts, role-based sessions and deterministic test data. It is maintained separately from the application repository so test code, reports and credentials remain isolated from product code.

## Current status

| Item | Current implementation |
|---|---|
| Manual test inventory | 172 cases across 17 modules |
| Executable automated checks | 63 collected tests: 55 application variants and 8 framework unit checks |
| Manual cases currently linked | 41 automated, 131 pending |
| UI automation | Playwright Page Object Model |
| API automation | Playwright `APIRequestContext` wrapper |
| Test runner | pytest 8 |
| Browsers | Chromium, Firefox and WebKit |
| Parallel execution | pytest-xdist |
| Reports | HTML, JUnit XML, screenshots, video and Playwright traces |
| CI | Always-on quality gate plus API, Chromium and nightly cross-browser jobs |

See [Automation Traceability](docs/automation-traceability.md) for the manual-to-automation mapping. Email delivery, payments, external issue creation, file storage, multi-user concurrency and destructive security testing require dedicated sandbox services.

## Application coverage

1. Landing page and navigation
2. Signup, login, logout, password reset and sessions
3. Pricing, plans, subscriptions and invoices
4. Boards, archived boards and Kanban lists
5. Cards, priority, severity, source and due dates
6. Labels, assignees, attachments and metadata
7. Global search and board filters
8. Invitations, share links, join requests and RBAC
9. Board and global reports
10. Notifications and preferences
11. Profile, password, theme and digest preferences
12. ClickUp/GitHub integration contracts
13. Security, accessibility and responsive checks
14. Cross-browser and end-to-end journeys

## Technology stack

| Component | Technology | Responsibility |
|---|---|---|
| UI automation | Playwright for Python | Browser workflows, assertions and evidence |
| API automation | Playwright request context | API contracts and setup/cleanup |
| Runner | pytest | Fixtures, markers and parametrization |
| Parallelism | pytest-xdist | Isolated concurrent execution |
| Configuration | python-dotenv | Environment loading |
| Validation | Ruff and compileall | Static quality checks |
| Reporting | pytest-html and JUnit | Human and CI reports |
| Schema support | jsonschema | Structured response validation |

## Framework architecture

```text
snagly-playwright-automation/
├── .github/workflows/playwright.yml # UI smoke and API quality gates
├── clients/snagly_api.py            # Central authenticated API wrapper
├── config/settings.py               # Typed environment configuration
├── docs/                            # Traceability, catalogue and data guidance
├── pages/                           # Page Objects and shared interactions
├── test_data/                       # 172-case registry and shared datasets
├── tests/api/                       # Public/authenticated API contracts
├── tests/e2e/                       # Browser journeys and responsive tests
├── utils/                           # Data, contract and accessibility helpers
├── conftest.py                      # Shared UI/API/RBAC/data fixtures
├── pytest.ini                       # Markers and pytest defaults
├── requirements.txt
└── ruff.toml
```

### Design rules

- Tests contain business intent; Page Objects contain selectors and interactions.
- API helpers create and clean up state; UI tests validate user-visible behavior.
- Prefer accessible roles, labels and placeholders over CSS classes.
- Obtain IDs from API responses; never hard-code database IDs.
- Generated records start with `E2E-` and include a unique run suffix.
- Keep tests independent, repeatable and safe to retry.
- Never commit credentials, tokens, production data or payment details.
- Do not use `time.sleep()`; use Playwright assertions and state waits.

## Fixtures

| Fixture | Purpose |
|---|---|
| `settings` | Session-scoped typed environment configuration |
| `app_url` | Configured frontend address |
| `page` | pytest-playwright browser page |
| `authenticated_page` | Owner session authenticated through UI |
| `page_as(role)` | Isolated Admin, Owner, Team, Client or Other Owner session |
| `api_client` | Fresh anonymous API request context |
| `authenticated_api` | Authenticated `SnaglyApi` client |
| `disposable_board` | Unique API-created board with teardown deletion |
| `disposable_list` | List under the disposable board |
| `disposable_card` | Unique card with teardown deletion |
| `test_data_registry` | Validated catalogue for all 172 manual cases |
| `case_data` | Automatically resolved data for the test's `case_id` marker |
| `case_user` | Environment credentials for the role assigned to that case |
| `test_file_factory` | Disposable exact-size attachment generator |

`page_as(role)` creates separate browser contexts so cookies, local storage and permissions do not leak between role or concurrency scenarios.

## Automatic test data

Every manual case from `SNAG-TC-001` to `SNAG-TC-172` has a record in `test_data/cases.json`. Add a `case_id` marker and request `case_data`; pytest automatically combines that record with the required shared boundary/security values, fresh entity names, relative dates, temporary storage and credentials from environment variables.

```python
@pytest.mark.case_id("SNAG-TC-001")
def test_landing_page(page, app_url, case_data):
    assert case_data.module == "Landing Page"
```

`test_data/common.json` contains only safe, non-secret values. `test_data/registry.py` injects secrets and run-specific values on demand. The catalogue validates its count, ID format and complete sequence at startup. See [Automatic Test Data](docs/test-data.md) for usage, regeneration and lifecycle rules.

## Prerequisites

- Python 3.12+
- Git
- Reachable Snagly frontend and FastAPI backend
- Chromium for development; Firefox and WebKit for release validation
- Dedicated test/staging accounts and database
- Node.js 20+ only when running Snagly locally

Do not point destructive or data-creation tests at production.

## Installation

### macOS or Linux

```bash
git clone https://github.com/klrahulindia22-afk/snagly-playwright-automation.git
cd snagly-playwright-automation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

### Windows PowerShell

```powershell
git clone https://github.com/klrahulindia22-afk/snagly-playwright-automation.git
cd snagly-playwright-automation
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env
```

For cross-browser execution:

```bash
playwright install chromium firefox webkit
```

## Environment configuration

Copy `.env.example` to `.env`. The `.env` file is ignored by Git.

```dotenv
BASE_URL=http://localhost:5275
API_BASE_URL=http://localhost:8000

TEST_USER_EMAIL=
TEST_USER_PASSWORD=
TEAM_USER_EMAIL=
TEAM_USER_PASSWORD=
CLIENT_USER_EMAIL=
CLIENT_USER_PASSWORD=
OTHER_OWNER_EMAIL=
OTHER_OWNER_PASSWORD=
ADMIN_EMAIL=
ADMIN_PASSWORD=

HEADLESS=true
DEFAULT_TIMEOUT_MS=10000
NAVIGATION_TIMEOUT_MS=20000
TEST_RUN_ID=local
```

| Variable | Required | Description |
|---|---:|---|
| `BASE_URL` | UI suites | React frontend URL |
| `API_BASE_URL` | API/data fixtures | FastAPI backend origin |
| `TEST_USER_*` | Authenticated suites | Dedicated Board Owner account |
| `TEAM_USER_*` | Permission suites | Team-member account |
| `CLIENT_USER_*` | Permission suites | Client account |
| `OTHER_OWNER_*` | Isolation suites | Owner of a separate board |
| `ADMIN_*` | Admin suites | Super Admin account |
| `HEADLESS` | No | `true` hides the browser; `false` shows it |
| `DEFAULT_TIMEOUT_MS` | No | Locator/assertion timeout; default 10 seconds |
| `NAVIGATION_TIMEOUT_MS` | No | Navigation timeout; default 20 seconds |
| `TEST_RUN_ID` | No | CI/build ID included in generated data |
| `TEST_ENVIRONMENT` | No | `local`, `staging` or explicitly authorized `production` |
| `ALLOW_DESTRUCTIVE_TESTS` | No | Explicit safety switch for destructive cases; default `false` |
| `ALLOW_PRODUCTION_TESTS` | No | Explicit authorization for production-like targets; default `false` |
| `FAIL_ON_BROWSER_ERRORS` | No | Fail UI tests on unexpected console/page errors; default `true` |
| `BROWSER_ERROR_ALLOWLIST` | No | Reviewed comma-separated error fragments to ignore |

`BASE_URL` and `API_BASE_URL` are intentionally separate because the Vite frontend and FastAPI backend may use different origins.

## Local Snagly environment

Use a dedicated test database. From the Snagly application repository:

```bash
cd backend
export TEST_DB_URL='mysql+aiomysql://USER:PASSWORD@localhost:3306/snagly_test'
python -m tests.seed
uvicorn main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev -- --port 5275
```

The seed should provide verified Owner, Team, Client, Other Owner and Super Admin accounts plus stable boards, columns, cards, labels, comments and checklists. See [Test Data](docs/test-data.md).

## Running tests

### Fast quality checks

```bash
python -m compileall -q conftest.py clients config pages test_data tests utils
python -m ruff check .
pytest --collect-only -q
pytest --collect-only -q --traceability-output=reports/traceability

pytest -m smoke --browser chromium
pytest -m public --browser chromium
pytest -m api
```

### Module suites

```bash
pytest -m auth --browser chromium
pytest -m boards --browser chromium
pytest -m cards --browser chromium
pytest -m permissions --browser chromium
pytest -m reports --browser chromium
pytest -m notifications --browser chromium
pytest -m profile --browser chromium
pytest -m security
pytest -m responsive --browser chromium
```

### Regression and evidence

```bash
pytest -m "regression and not destructive" --browser chromium

pytest --browser chromium \
  --tracing retain-on-failure \
  --screenshot only-on-failure \
  --video retain-on-failure \
  --junitxml=reports/junit.xml \
  --html=reports/report.html \
  --self-contained-html

pytest tests/e2e/test_login.py --browser chromium --headed --slowmo 300
```

### Cross-browser and parallel execution

```bash
pytest -m smoke --browser chromium
pytest -m smoke --browser firefox
pytest -m smoke --browser webkit

pytest -n auto -m "regression and not serial" --browser chromium
```

Use parallel execution only when data is isolated. Shared records and provider integrations should use the `serial` marker.

## Markers

| Marker | Scope |
|---|---|
| `smoke` | Critical deployment checks |
| `regression` | Broader functional regression |
| `public` | Landing, pricing and account-entry pages |
| `auth` | Signup, login, reset, sessions and 2FA |
| `boards` | Board, list and Kanban workflows |
| `cards` | Card lifecycle and metadata |
| `permissions` | Owner, Team, Client and Admin RBAC |
| `reports` | Dashboards and exports |
| `notifications` | Notifications and preferences |
| `profile` | User profile and preferences |
| `integrations` | Provider configuration and issue push |
| `api` | Backend contracts |
| `security` | Authentication/authorization regression |
| `accessibility` | Accessibility-focused checks |
| `responsive` | Viewport and reflow checks |
| `destructive` | Permanent deletion or mutation |
| `serial` | Must not run concurrently |
| `case_id(...)` | Manual case IDs covered by the test or parameter |

Examples:

```bash
pytest -m "smoke and not destructive"
pytest -m "api and security"
pytest -m "boards or cards"
```

## Adding automation

### UI test

1. Add selectors and interactions under `pages/`.
2. Use API fixtures for setup and cleanup.
3. Keep outcome assertions in the test.
4. Add functional and execution markers.
5. Run the focused test, module suite and smoke suite.

```python
import pytest
from playwright.sync_api import expect

from pages.board_page import BoardPage


@pytest.mark.boards
@pytest.mark.cards
def test_api_created_card_is_visible(authenticated_page, app_url, disposable_board, disposable_card):
    board = BoardPage(authenticated_page, app_url)
    board.open_by_id(disposable_board["id"])
    expect(authenticated_page.get_by_text(disposable_card["title"], exact=True)).to_be_visible()
```

### API test

Extend `clients/snagly_api.py` rather than duplicating endpoint calls.

```python
import pytest

from utils.contracts import assert_collection


@pytest.mark.api
@pytest.mark.boards
def test_boards_contract(authenticated_api):
    boards = assert_collection(authenticated_api.get_boards())
    for board in boards:
        assert {"id", "name", "slug", "my_role"}.issubset(board)
```

### Test-data rules

- Use stable catalog values for read-only assertions.
- Use `unique_name()` for created records.
- Never depend on numeric IDs.
- Clean data in fixture teardown even after failures.
- Keep destructive tests out of normal smoke runs.

## Reports and debugging

| Artifact | Purpose |
|---|---|
| HTML | Human-readable execution summary |
| JUnit XML | CI reporting |
| Screenshot | UI state on failure |
| Video | Failed browser session |
| Trace | DOM, network, console and action timeline |

```bash
playwright show-trace test-results/<test-folder>/trace.zip
pytest path/to/test.py::test_name --headed --slowmo 500 -s
pytest path/to/test.py::test_name --tracing on
pytest -x --tb=long
```

## CI/CD

`.github/workflows/playwright.yml` contains:

| Job | Purpose | Requirement |
|---|---|---|
| `quality-gates` | Lint, compile, dependency, unit, collection and traceability checks | None |
| `ui-smoke` | Chromium UI smoke with evidence | Frontend/API URL and Owner credentials |
| `api-contracts` | API contracts and reports | Backend URL and Owner credentials |
| `cross-browser-nightly` | Firefox and WebKit smoke | Scheduled/manual run and staging secrets |
| `regression-nightly` | Chromium non-destructive regression with video/trace evidence | Scheduled/manual run and staging secrets |

Configure GitHub Actions secrets:

| Secret | Purpose |
|---|---|
| `SNAGLY_BASE_URL` | Reachable test/staging frontend |
| `SNAGLY_API_BASE_URL` | Reachable FastAPI backend |
| `SNAGLY_TEST_USER_EMAIL` | Dedicated Owner automation account |
| `SNAGLY_TEST_USER_PASSWORD` | Owner password |
| `SNAGLY_TEAM_USER_EMAIL/PASSWORD` | Team-member permission checks |
| `SNAGLY_CLIENT_USER_EMAIL/PASSWORD` | Client permission checks |
| `SNAGLY_OTHER_OWNER_EMAIL/PASSWORD` | Data-isolation checks |
| `SNAGLY_ADMIN_EMAIL/PASSWORD` | Admin checks |

The workflow runs on pushes to `main`, pull requests, manual dispatch and a nightly schedule. The quality gate always runs. Live jobs report a notice and skip their execution step when staging secrets are absent. GitHub-hosted runners cannot access localhost or a developer laptop.

## Quality gates

Before committing:

```bash
python -m compileall -q conftest.py clients config pages test_data tests utils
python -m ruff check .
pytest tests/unit -q
pytest --collect-only -q --traceability-output=reports/traceability
```

A change is complete when tests collect, lint and compilation pass; data is isolated and cleaned; no secrets or reports are tracked; and Page Objects, clients, fixtures, tests and documentation remain aligned.

## Environment-dependent coverage

| Area | Dependency |
|---|---|
| Signup/reset email | Test mailbox or email capture |
| Multi-role permissions | Owner, Team, Client and Other Owner accounts |
| Attachments | Isolated object storage and permitted files |
| CSV/PDF export | Downloads and deterministic data |
| ClickUp/GitHub push | Provider sandbox and scoped token |
| Subscriptions | Stripe/Razorpay sandbox |
| Admin workflows | Super Admin account |
| WebSocket/concurrency | Two isolated contexts |
| Load/performance | Dedicated load environment |
| Full security testing | Explicitly authorized environment |

## Troubleshooting

| Problem | Resolution |
|---|---|
| Browser executable missing | Run `playwright install chromium` |
| Browser cannot reach site | Verify URL, DNS, VPN/proxy and environment availability |
| API tests fail immediately | Verify backend URL, health and network access |
| Auth tests are skipped | Configure Owner credentials |
| Role test is skipped | Configure that role in `.env` |
| Login is rejected | Confirm account is verified and 2FA is disabled for automation |
| Plan limit blocks fixture | Use a suitable test plan or remove stale `E2E-` data |
| CI job is skipped | Configure the required URL secret |
| Locator fails after release | Inspect trace and update the Page Object |
| Parallel test is flaky | Isolate data or use `serial` |
| Export fails | Verify downloads and backend storage |

## Security and safety

- Use dedicated automation accounts and sandbox integrations.
- Never automate using personal or production credentials.
- Never commit `.env`, tokens, passwords or customer files.
- Keep provider tokens least-privileged and rotate them regularly.
- Treat screenshots, traces and videos as potentially sensitive.
- Require explicit authorization for destructive, security or load testing.

## Related resources

- [Snagly application](https://github.com/klrahulindia22-afk/snagly)
- [Automation repository](https://github.com/klrahulindia22-afk/snagly-playwright-automation)
- [Automation Traceability](docs/automation-traceability.md)
- [Test Data](docs/test-data.md)
- [Test Case Catalogue](docs/test-case-catalogue.md)
- [Live Deployment Test Cases](docs/live-deployment-test-cases.md)

When behavior changes, update the Page Object, API client, fixtures/data, automated tests and documentation together.

# Snagly Automation Framework

This repository is the independent Python + Playwright quality-automation project for Snagly. It tests the live React interface and FastAPI backend without copying application source code or storing production credentials.

## Framework coverage

| Layer | Tooling | Purpose |
|---|---|---|
| Browser UI | Playwright + Page Objects | Validate real user workflows |
| Backend API | Playwright request context | Verify FastAPI responses and controlled setup |
| Test data | Idempotent seed + catalog | Stable roles, boards, cards, labels, comments and checklists |
| Reporting | JUnit, HTML, traces, screenshots and video | Failure evidence for developers |
| CI | GitHub Actions | Smoke checks against a reachable test/staging environment |

## Repository layout

~~~text
clients/        API wrappers; no UI selectors
config/         Environment configuration only
pages/          Page Objects: locators and user interactions
test_data/      Stable names for controlled test records
tests/api/      Fast backend/API contract checks
tests/e2e/      Browser journeys and permission scenarios
docs/           Test-data and framework documentation
.github/        CI workflow
conftest.py     Shared fixtures, timeouts and browser/API contexts
~~~

## Prerequisites

- Python 3.12+
- Node.js 20+ to run the Snagly UI
- Snagly frontend, FastAPI backend and a dedicated MySQL test database
- A dedicated test account. Never use a personal or production account.

## Local installation

~~~bash
git clone https://github.com/klrahulindia22-afk/snagly-playwright-automation.git
cd snagly-playwright-automation
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
~~~

Configure .env:

~~~dotenv
BASE_URL=http://localhost:5275
API_BASE_URL=http://localhost:8000
TEST_USER_EMAIL=owner@test.com
TEST_USER_PASSWORD=Owner@1234
HEADLESS=true
~~~

BASE_URL is the React UI and API_BASE_URL is the FastAPI backend. Keep them separate. The .env file is ignored by Git and must never be committed.

## Prepare application test data

Use a dedicated test database only:

~~~bash
cd backend
export TEST_DB_URL='mysql+aiomysql://USER:PASSWORD@localhost:3306/snagly_test'
python -m tests.seed
uvicorn main:app --reload --port 8000
~~~

In another terminal:

~~~bash
cd frontend
npm install
npm run dev -- --port 5275
~~~

The seed creates verified role-based users; the Test Board; Backlog, In Progress, Review and Done columns; cards across states; labels; assignees; comments; and checklist data. See [test-data.md](docs/test-data.md) for the complete catalog.

## Run tests

~~~bash
# Critical checks, visible Chromium
pytest -m smoke --browser chromium --headed

# Authentication checks
pytest -m auth --browser chromium

# Backend/API checks only
pytest -m api

# Complete suite with reports and failure evidence
pytest --browser chromium --tracing retain-on-failure --screenshot only-on-failure \
  --video retain-on-failure --junitxml=reports/junit.xml \
  --html=reports/report.html --self-contained-html

# Parallel smoke suite: use only when data isolation is assured
pytest -n auto -m smoke --browser chromium

# Cross-browser release checks
pytest -m smoke --browser chromium
pytest -m smoke --browser firefox
pytest -m smoke --browser webkit
~~~

Inspect a failed Playwright trace:

~~~bash
playwright show-trace test-results/<test-folder>/trace.zip
~~~

## Test-data governance

Stable seed-data names are defined in test_data/catalog.py. Use these names rather than numeric database IDs.

| Role | Coverage |
|---|---|
| Super Admin | Admin panel, users, plans and limits |
| Board Owner | Boards, membership and full card management |
| Team Member | Bug updates, comments, assignment and movement |
| Client | Permitted bug access and restrictions |
| Other Owner | Negative board-isolation scenarios |

Seed records are read-only. New data must start with E2E- plus a unique run suffix and must be removed in teardown.

## How to add a UI test

1. Confirm the feature requirement and expected behaviour for every relevant role.
2. Add locators and actions in the applicable Page Object under pages/.
3. Use accessible role/name selectors. If an element lacks a unique accessible identity, ask development to add a data-testid. Do not use CSS classes or nth selectors.
4. Write the business scenario in tests/e2e/, with correct pytest markers.
5. Use API helpers only for setup/cleanup; validate the business action through the UI.
6. Run the focused test, then the related smoke or regression group.

Example:

~~~python
@pytest.mark.boards
@pytest.mark.regression
def test_owner_can_create_a_board(authenticated_page):
    boards = BoardsPage(authenticated_page)
    boards.create_board("E2E-Release-board")
    expect(authenticated_page.get_by_text("E2E-Release-board")).to_be_visible()
~~~

## How to add an API test

Use clients/snagly_api.py, not repeated raw HTTP logic. Every API test must assert status and response contract, including negative permission cases.

~~~python
@pytest.mark.api
def test_plans_response_contains_data(api_client):
    response = SnaglyApi(api_client).get_public_plans()
    expect(response).to_be_ok()
    assert "data" in response.json()
~~~

## Markers

| Marker | Meaning |
|---|---|
| smoke | Mandatory high-value deployment checks |
| auth | Signup, login, reset password and 2FA |
| boards | Board, list, card and Kanban workflows |
| permissions | Owner, Team, Client and Admin access rules |
| api | FastAPI endpoint and response-contract checks |
| regression | Broader pre-release/nightly coverage |

## CI/CD configuration

GitHub-hosted runners cannot access a laptop's localhost. Use a reachable staging/test environment and add these repository secrets:

| Secret | Purpose |
|---|---|
| SNAGLY_BASE_URL | Staging/test frontend URL |
| SNAGLY_TEST_USER_EMAIL | Dedicated automation account |
| SNAGLY_TEST_USER_PASSWORD | Dedicated automation-account password |

The included workflow runs on main-branch pushes, pull requests and manual dispatch. It uploads test evidence after execution.

## Quality standards

- Never commit credentials, production data, payment details, API tokens or sensitive screenshots.
- Never use time.sleep(); wait for visible product state with Playwright assertions.
- Keep every test independent, repeatable and safe to retry.
- Prefer API setup plus UI verification to reduce slow browser preparation.
- Keep Page Objects for interactions and tests for business intent.
- Preserve a trace, screenshot, video and JUnit result for failures.
- Run ruff check . and python -m compileall -q conftest.py clients config pages test_data tests before a pull request.

## Coverage roadmap

1. Authentication and session handling.
2. Board/list/card CRUD, filters and drag/drop.
3. Labels, assignees, attachments, comments, checklists, due dates and custom fields.
4. Role permissions and client data isolation.
5. Dashboards, notifications, export/import, templates, integrations and SLA rules.
6. Subscription/payment sandbox and admin workflows.
7. Accessibility, responsive UI, cross-browser, performance and security regression checks.

## Troubleshooting

| Issue | Check |
|---|---|
| Browser cannot connect | URLs in .env and running frontend/backend processes |
| Login rejected | Active verified test account and correct seed database |
| API tests fail locally | API_BASE_URL, backend port and CORS settings |
| CI is skipped | SNAGLY_BASE_URL is missing; GitHub cannot access localhost |
| Flaky result | Inspect trace/screenshot, then improve selector or state wait |

When a product feature changes, update the Page Object, test data, scenario and relevant documentation in the same pull request.

# Snagly Playwright Automation

Python + Playwright end-to-end automation for the Snagly web application. The suite is intentionally kept in its own repository and tests the deployed/running application as a user would.

## Included now

- Page Object Model foundation
- Configurable base URL and test credentials via `.env`
- Login-page smoke checks and authenticated login check
- First authenticated boards smoke check
- Screenshots and Playwright traces on failure
- GitHub Actions workflow for a publicly reachable staging environment

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

Update `.env` with your test account. Keep the current local address as `BASE_URL=http://localhost:5275`.

## Run tests

```bash
# Critical unauthenticated checks
pytest -m smoke --browser chromium --headed

# All login checks, including a real test account
pytest -m auth --browser chromium --tracing retain-on-failure --screenshot only-on-failure
```

Never commit `.env`, account passwords, API tokens, or payment-gateway keys.

## CI setup

For the GitHub Actions job, configure these repository secrets:

- `SNAGLY_BASE_URL` — a staging/test URL reachable from GitHub Actions
- `SNAGLY_TEST_USER_EMAIL`
- `SNAGLY_TEST_USER_PASSWORD`

The workflow deliberately skips when no staging URL is configured, because GitHub-hosted runners cannot access a laptop's `localhost`.

## Next test coverage

1. Board creation and board access by role
2. Create, edit, assign, move, and close bug cards
3. Labels, attachments, comments, due dates, and checklists
4. Permission checks for Owner, Team Member, Client, and Super Admin
5. Dashboard, notification, integration, and admin scenarios

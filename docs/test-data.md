# Automatic test-data management

The framework contains a validated data record for every manual test case from `SNAG-TC-001` through `SNAG-TC-172`. Tests request `case_data`; pytest reads the test's `case_id` marker and resolves the right static, generated and secret values only when that test executes.

## Data layers

| Layer | Source | Purpose |
|---|---|---|
| Case catalogue | `test_data/cases.json` | Module, scenario, priority, role, review status and required data groups for all 172 cases |
| Shared safe data | `test_data/common.json` | Boundaries, valid/invalid inputs, security payloads, viewports and attachment specifications |
| Runtime data | `test_data/registry.py` | Environment credentials, unique entity names, relative dates and a per-test temporary directory |

Secrets are never stored in JSON. Owner, Admin, Team, Client and Other Owner credentials are read from `.env` through `Settings`. Unique names include `TEST_RUN_ID`; dates are calculated at execution time; temporary files are removed by pytest.

## Automatic lookup

```python
import pytest


@pytest.mark.case_id("SNAG-TC-009")
def test_valid_login(page, app_url, case_data, case_user):
    assert case_data.scenario
    page.goto(f"{app_url}/login")
    # case_user contains credentials for the role assigned to SNAG-TC-009.
```

Resolution is automatic:

1. pytest finds `@pytest.mark.case_id("SNAG-TC-...")`.
2. `case_data` asks the session-scoped registry for that ID.
3. The registry merges the case's referenced groups from `common.json`.
4. It injects runtime credentials, unique names, dates and `tmp_path`.
5. JSON Schema plus registry rules reject unknown, incomplete, duplicate or wrongly referenced data.

| Fixture | Result |
|---|---|
| `test_data_registry` | Validated full catalogue, loaded once per pytest session |
| `case_data` | Metadata and merged values for the current `case_id` |
| `case_user` | Credentials for the case's assigned role; skips clearly when unset |
| `test_file_factory` | Exact-size disposable files for upload boundary tests |

Example value access:

```python
valid_email = case_data.values["emails"]["valid"]
xss_payloads = case_data.values["security_payloads"]["xss"]
board_name = case_data.values["unique"]["board"]
future_date = case_data.values["dates"]["future"]
```

Only groups listed in a case's `data_refs` are merged. Runtime values (`users`, `unique`, `dates`, `temp_dir`) are always available.

## Regenerating from the master workbook

When the approved workbook changes, regenerate the case catalogue rather than editing 172 records manually:

```bash
python scripts/generate_case_data.py /path/to/Snagly_Complete_App_Test_Cases.xlsx \
  --output test_data/cases.json
pytest tests/unit/test_test_data_registry.py -q
```

The generator infers the role and required shared datasets from the module, type, scenario and original test-data description while preserving the workbook text for traceability. Generated records are marked `generated_needs_review`; a QA reviewer must verify the role and references before changing that value to `reviewed`. Review the JSON diff and commit it with the workbook change reference.

## Seeded application data

For tests that need persistent relationships, seed a dedicated test database from the Snagly application repository. Never run the seed against production.

```bash
cd backend
export TEST_DB_URL='mysql+aiomysql://USER:PASSWORD@localhost:3306/snagly_test'
python -m tests.seed
```

The environment should contain verified Owner, Admin, Team, Client and Other Owner accounts, an accessible board with Kanban lists/cards/labels, and a separate private board for isolation checks. Configure credentials in `.env`; shared CI environments must use secret storage.

## Lifecycle rules

- Prefer API-created disposable records and delete them in fixture teardown.
- Never hard-code database IDs; retain IDs returned by the API.
- Never commit credentials, tokens, customer data or real payment details.
- Generate uploads through `test_file_factory`; do not commit large binaries.
- Use sandbox services for email, payments, integrations and destructive security payloads.
- Run parallel workers with distinct `TEST_RUN_ID` values when the environment does not provide build-specific IDs.

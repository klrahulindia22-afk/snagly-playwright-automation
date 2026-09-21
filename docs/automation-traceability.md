# Automation traceability

The manual suite contains 172 test cases across 17 modules. This repository separates them into three execution layers:

1. **Executable UI/API regression** — stable flows implemented in `tests/e2e` and `tests/api`.
2. **Environment-dependent automation** — RBAC, email, payment, external integrations, downloads, file storage and concurrency require the documented role accounts or sandbox services.
3. **Specialist validation** — penetration testing, load testing and full WCAG audits remain dedicated quality activities; Playwright provides release sanity coverage only.

| Manual suite module | Framework implementation |
|---|---|
| Landing Page | `pages/public_pages.py`, `test_public_pages.py` |
| Authentication | `pages/login_page.py`, signup/forgot objects, UI and API negative tests |
| Pricing & Subscription | Pricing object, public plan contract, subscription/invoice client methods |
| Boards | `BoardsPage`, disposable board fixture, UI and API lifecycle tests |
| Lists | API list fixture/client and board workflow assertions |
| Cards | `BoardPage`, disposable card fixture, CRUD/update contract tests |
| Attachments | File-ready card object and API client extension point; sandbox storage required |
| Search & Filters | Global navigation search and board filter objects/tests |
| Sharing & Roles | Share dialog checks and isolated `page_as(role)` sessions |
| Reports | `ReportsPage`, board/global dashboard contracts, download helper path |
| Notifications | Notification page and notification/prefs API contracts |
| Profile & Preferences | `ProfilePage`, theme/session/profile checks |
| Integrations | Board integration contract client; provider sandbox required for push tests |
| Security | Anonymous protection, non-disclosure and role-isolation foundations |
| Accessibility | Reusable accessible-name and overflow assertions |
| Compatibility & Performance | Browser/viewport matrices through pytest-playwright and CI |
| End-to-End | API setup + UI verification fixtures support independent full journeys |

Every destructive test must use `E2E-` data, declare the `destructive` marker, and clean up through a fixture finalizer. Credentials and provider tokens remain environment secrets.

## Case-level report

Every application test and parameter must declare `@pytest.mark.case_id(...)`. Collection fails when the marker is missing. Generate the current 172-case status report with:

```bash
pytest --collect-only -q --traceability-output=reports/traceability
```

This creates JSON and Markdown reports showing each case as `automated` or `pending` and lists the collected test node IDs. The generated report is uploaded by the CI quality gate and is the authoritative automation-coverage view; the module table above describes architecture only.

# Snagly controlled test data

Run the following from the Snagly application repository after configuring a **dedicated test database**. Never run it against production data.

```bash
cd backend
export TEST_DB_URL='mysql+aiomysql://USER:PASSWORD@localhost:3306/snagly_test'
python -m tests.seed
```

The seed is idempotent: it can be run again without creating duplicate users, boards, columns, cards, labels, comments, or checklist items.

## Test users

| Purpose | Email | Password | Role |
|---|---|---|---|
| Admin checks | `admin@test.com` | `Admin@1234` | Super Admin |
| Owner workflows | `owner@test.com` | `Owner@1234` | Board Owner |
| Team workflows | `team@test.com` | `Team@1234` | Team Member |
| Client restrictions | `client@test.com` | `Client@1234` | Client |
| Access-control negative checks | `other@test.com` | `Other@1234` | Other Board Owner |

These credentials are development-only fixtures. Replace them with CI secrets when the test environment is shared.

## Front-end test scenarios

| Data set | What it verifies |
|---|---|
| `Test Board` | Board landing, filters, columns, drag/drop, counts, and role-based visibility |
| Backlog / In Progress / Review / Done | Kanban ordering and state transitions |
| Critical login bug | Priority, severity, client source, assignee, checklist, and comments |
| UI / Regression / Client Reported labels | Label filtering and badge display |
| Completed profile card | Completed-card display and closed-state regression tests |
| `Other Board` | User-data isolation: the Client must not see this board |

## Back-end/API test scenarios

- Authentication: verified active users for each role.
- Authorization: Owner and Team can update board work; Client cannot alter lists or labels.
- Card payloads: urgent/high/normal/low priorities, critical/high/medium/low severities, internal/client sources, due dates, and complete state.
- Related records: labels, assignees, checklist progress, and comments.
- Isolation: one board with membership and one private board without Client membership.

The automation project exposes all stable names through `test_data/catalog.py`; UI/API tests should reference those constants rather than numeric database IDs.

# Snagly Complete Test-Case Catalogue

This catalogue is traceable to `docs/PRD.md` in the Snagly application repository. **Status rule:** the current repository has only the initial smoke/API scenarios automated; all remaining rows are the approved automation backlog until validated against a runnable test environment. Do not report a case as automated merely because it is listed here.

| Status | Meaning |
|---|---|
| Implemented | Automated, code-reviewed and executed against the target environment |
| Ready | Test design complete; selector/API and test data are known |
| Blocked | Requires a test environment, sandbox, email inbox, integration account or missing stable selector |

## Traceability and execution rules

- Each test must reference its ID in the pytest test name/docstring and its corresponding PRD module.
- P0 tests are mandatory deployment smoke/regression checks; P1 tests run pre-release; P2 tests run nightly or after relevant change.
- Payment, email, webhook and third-party integration scenarios must run only with sandbox/test credentials.
- Every destructive test uses unique `E2E-<run-id>` data and cleans up after itself.

## Authentication & security

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| AUTH-001 | Open login | Submit blank form | Email and password required messages | P0 | UI | Ready |
| AUTH-002 | Open login | Enter invalid email | Email format validation appears | P1 | UI | Ready |
| AUTH-003 | Verified active account | Log in with valid credentials | Redirect to My Boards and create session | P0 | UI/API | Ready |
| AUTH-004 | Account exists | Log in with wrong password | Generic invalid-credential error; no token | P0 | UI/API | Ready |
| AUTH-005 | Unverified account | Log in | Verification-required state shown | P0 | API/UI | Ready |
| AUTH-006 | Active session | Refresh page | Session refreshes without unexpected logout | P0 | UI/API | Ready |
| AUTH-007 | Existing user | Request password reset | Confirmation shown without exposing account existence | P1 | API/UI | Ready |
| AUTH-008 | Valid reset token | Set valid replacement password | Password changes and old password fails | P0 | API/UI | Ready |
| AUTH-009 | Logged-in user | Change profile password | Current password validated and session security maintained | P1 | UI/API | Ready |
| AUTH-010 | Eligible user | Set up, confirm and disable TOTP 2FA | 2FA state and recovery codes handled correctly | P0 | UI/API | Ready |
| AUTH-011 | 2FA-enabled user | Login with TOTP, email OTP and backup code | Only valid second factor grants a session | P0 | API/UI | Ready |
| AUTH-012 | Repeated failed login | Exceed configured attempt threshold | Account lockout and expiry behave as configured | P0 | API | Ready |
| AUTH-013 | Unauthenticated user | Open protected route | Redirect to login with safe return path | P0 | UI | Ready |
| AUTH-014 | Authenticated non-admin | Open admin route | Redirect/deny without data leakage | P0 | UI/API | Ready |
| AUTH-015 | Logged-in user | Log out | Tokens/session state removed and protected route inaccessible | P0 | UI | Ready |

## Boards, lists and membership

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| BOARD-001 | Owner logged in | Create board with valid name, description and colour | Board appears in My Boards with owner membership | P0 | UI/API | Ready |
| BOARD-002 | Owner logged in | Create board with blank/duplicate-edge name | Validation and unique slug behaviour are correct | P1 | UI/API | Ready |
| BOARD-003 | Existing board | Edit board name, description and colour | Changes persist and are visible after refresh | P1 | UI/API | Ready |
| BOARD-004 | Board owner | Archive and restore board | Archived board disappears/restores in correct views | P1 | UI/API | Ready |
| BOARD-005 | Board owner | Delete board | Confirmation, permission check and data removal are correct | P0 | UI/API | Ready |
| BOARD-006 | Owner with plan limit | Create beyond board limit | Creation denied with clear upgrade/limit message | P0 | API/UI | Ready |
| BOARD-007 | Board member | View My Boards and search by board name | Only accessible boards return; search is case-safe | P1 | UI/API | Ready |
| BOARD-008 | Owner board | Create, rename, reorder and delete lists | Order and state persist after refresh | P0 | UI/API | Ready |
| BOARD-009 | List with WIP limit | Create cards until and beyond limit | Limit warning/enforcement behaves as configured | P1 | API/UI | Ready |
| BOARD-010 | Client member | Attempt list create/edit/delete/reorder | Action is denied; existing lists remain unchanged | P0 | API/UI | Ready |
| BOARD-011 | Owner and existing user | Invite Team and Client roles | Invitation, expiry and reserved member limit are correct | P0 | API/UI | Ready |
| BOARD-012 | Valid invite | Accept as existing user and as new user | Correct membership, role and onboarding result | P0 | UI/API | Ready |
| BOARD-013 | Owner board | Change/remove member role | Updated access takes effect immediately | P0 | API/UI | Ready |
| BOARD-014 | Board with sharing | Create/revoke share link | Link grants only intended access and revoked link fails | P1 | UI/API | Ready |
| BOARD-015 | Public share link | Submit and review join request | Owner can approve/decline and requester state updates | P1 | UI/API | Ready |
| BOARD-016 | Client user | Request inaccessible board or board card | 403/not-found behaviour has no data disclosure | P0 | API | Ready |
| BOARD-017 | Board actions performed | Open activity feed | Relevant actor, action, time and object are recorded | P1 | UI/API | Ready |

## Cards and bug reporting

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| CARD-001 | Owner/Team with board access | Create card from quick/add-card form | Title, column, creator and default source are correct | P0 | UI/API | Ready |
| CARD-002 | Client member | Create a card | Card source is Client regardless of submitted source | P0 | API/UI | Ready |
| CARD-003 | Card exists | Edit title, description, priority, severity and dates | All changed values persist and audit activity is created | P0 | UI/API | Ready |
| CARD-004 | Card exists | Submit blank/oversized title | Validation prevents invalid card creation/update | P0 | API/UI | Ready |
| CARD-005 | Cards in multiple columns | Drag/move card between lists and positions | List, ordering and live UI update are correct | P0 | UI/API | Ready |
| CARD-006 | Card exists | Mark complete/uncomplete | Completion state and card display update correctly | P1 | UI/API | Ready |
| CARD-007 | Card exists | Archive, restore, soft-delete and permanently delete | Correct lifecycle state and permissions apply | P0 | API/UI | Ready |
| CARD-008 | Existing card | Duplicate card | New record has expected copied/not-copied fields and order | P1 | UI/API | Ready |
| CARD-009 | Multiple selected cards | Apply supported bulk action | Only permitted selected cards change | P1 | UI/API | Ready |
| CARD-010 | Card with due/start dates | Set valid, invalid and past date combinations | Date validation, display timezone and sort are correct | P1 | UI/API | Ready |
| CARD-011 | SLA rule exists | Create severity-matched card without due date | SLA due date and activity entry are generated | P1 | API/UI | Ready |
| CARD-012 | Card form | Capture browser/OS/viewport metadata | Metadata persists and is displayed only where authorised | P2 | API | Ready |
| CARD-013 | Card with recurrence | Create, edit, trigger and stop recurrence | Next occurrence and end-date logic are correct | P1 | API/UI | Ready |
| CARD-014 | Card data | Filter by label, assignee, priority, severity, source, due date and completion | Result set and clear-filters state are correct | P0 | UI/API | Ready |
| CARD-015 | Card data | Search card title/description | Results are relevant, scoped to access and safely escaped | P1 | UI/API | Ready |
| CARD-016 | Mobile viewport | Create/open/edit/move card | Core card workflow remains usable and responsive | P1 | UI | Ready |

## Card collaboration

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| COLLAB-001 | Labels available | Create, rename, recolour and delete label | Label lifecycle and board scope are correct | P1 | UI/API | Ready |
| COLLAB-002 | Client member | Attempt label CRUD | Action is denied | P0 | API/UI | Ready |
| COLLAB-003 | Card and labels | Add/remove card labels | Badges and filtered results update correctly | P1 | UI/API | Ready |
| COLLAB-004 | Board members | Assign/unassign one or more users | Assignments, notifications and UI chips update | P0 | UI/API | Ready |
| COLLAB-005 | Card exists | Add/edit/delete comment | Authorisation, soft deletion and chronological display are correct | P0 | UI/API | Ready |
| COLLAB-006 | Comment with mention | Mention member and @board | Correct recipients receive in-app/email notifications once | P1 | API/UI | Ready |
| COLLAB-007 | Comment exists | Add/edit/delete reply | Thread order and authorisation are correct | P1 | UI/API | Ready |
| COLLAB-008 | Card exists | Create checklist, add/reorder/edit/check/delete items | Progress count and assignee/due-date display are correct | P0 | UI/API | Ready |
| COLLAB-009 | Card exists | Watch/unwatch card | Watcher count and subsequent notification behaviour are correct | P1 | API/UI | Ready |
| COLLAB-010 | Attachment-enabled plan | Upload, preview, download and delete permitted file | Type/size/storage limits and authorisation are enforced | P0 | UI/API | Ready |
| COLLAB-011 | Card custom fields configured | Set/clear supported field values | Type validation and UI display are correct | P1 | UI/API | Ready |
| COLLAB-012 | Card has history | Open card activity | Every displayed change has correct actor and timestamp | P1 | UI/API | Ready |
| COLLAB-013 | Card template available | Create, edit, apply and delete template | Template creates correct independent card data | P1 | UI/API | Ready |

## Search, notifications, dashboard and profile

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| UX-001 | Multiple boards/cards | Use global search | Results are relevant, keyboard navigable and access-scoped | P1 | UI/API | Ready |
| UX-002 | Eligible plan | Open command palette with Ctrl/Cmd+K | Palette opens, searches and closes correctly | P1 | UI | Ready |
| UX-003 | Shortcut overlay | Use documented keyboard shortcuts | Each shortcut performs only its documented action | P2 | UI | Ready |
| UX-004 | Unread notifications | Open bell/page, mark one/all read | Counts and read state persist | P0 | UI/API | Ready |
| UX-005 | Notification preferences | Enable/disable event/browser/email preferences | Only selected delivery channels are used | P1 | UI/API | Ready |
| UX-006 | Digest configured | Update digest preference and trigger test digest | Timing/preference and content selection are correct | P1 | API | Ready |
| UX-007 | Board has seeded cards | Open board dashboard/reports | Counts, trends, severity, workload and resolution metrics match source data | P1 | UI/API | Ready |
| UX-008 | Multiple accessible boards | Open global dashboard | Aggregate data excludes inaccessible boards | P1 | UI/API | Ready |
| UX-009 | User profile | Update profile, avatar/initial colour and settings | Changes persist and validate correctly | P1 | UI/API | Ready |
| UX-010 | User profile | View profile My Boards section | Board visibility and navigation are correct | P2 | UI | Ready |
| UX-011 | Board/card data | Export CSV/PDF and import valid/invalid CSV | Data integrity, validation and permission rules apply | P1 | UI/API | Ready |
| UX-012 | Archived content | Search/archive views | Archived records obey filter and restore behaviour | P1 | UI/API | Ready |

## Integrations, plans and billing

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| INT-001 | Owner with integration feature | Create/update/delete ClickUp integration | Credentials are encrypted and never exposed in response/UI | P0 | API/UI | Ready |
| INT-002 | Owner with integration feature | Create/update/delete GitHub/GitLab integration | Repository configuration validation works | P1 | API/UI | Ready |
| INT-003 | Configured integration | Push card and retry simulated failure | External reference, success/failure state and retry feedback are correct | P0 | API | Ready |
| INT-004 | Public visitor | View landing, pricing and plan details | Plan information is accurate and navigation works | P1 | UI/API | Ready |
| BILL-001 | Authenticated user | View current subscription and invoices | Only own records and correct plan state are visible | P0 | UI/API | Ready |
| BILL-002 | Sandbox gateway configured | Start checkout for Stripe/Razorpay | Correct gateway, amount, currency and return handling are used | P0 | API/UI | Ready |
| BILL-003 | Payment confirmed webhook | Process valid Stripe/Razorpay event | Subscription changes exactly once and audit/webhook record is stored | P0 | API | Ready |
| BILL-004 | Invalid/duplicate webhook | Post invalid signature and duplicate event | Rejected or idempotently ignored without plan change | P0 | API | Ready |
| BILL-005 | Active subscription | Upgrade, downgrade, cancel, reactivate and switch billing cycle | Effective dates, entitlement and invoice state are correct | P0 | API/UI | Ready |
| BILL-006 | Coupon available | Validate and apply valid/invalid/expired coupon | Discount and eligibility rules are accurate | P1 | API/UI | Ready |
| BILL-007 | Saved method exists | List and remove payment method | Only owned method can be viewed/removed | P1 | API | Ready |

## Admin, resilience and non-functional

| ID | Preconditions | Action | Expected result | Priority | Target | Status |
|---|---|---|---|---|---|---|
| ADMIN-001 | Super Admin | Log in to separate admin panel | Admin dashboard loads and non-admin is denied | P0 | UI/API | Ready |
| ADMIN-002 | Super Admin | Create, deactivate, reset and change role of users | Restrictions and audit log are enforced | P0 | UI/API | Ready |
| ADMIN-003 | Super Admin | View/manage boards and member limits | Limits affect board behaviour correctly | P1 | UI/API | Ready |
| ADMIN-004 | Super Admin | View/cancel pending invites | Invite status and access update correctly | P1 | UI/API | Ready |
| ADMIN-005 | Super Admin | Manage plans, feature flags, coupons and gateway config | Validation, publishing and permission checks work | P0 | UI/API | Ready |
| ADMIN-006 | Super Admin | View revenue, subscriptions and stats | Totals/filters match seeded records | P1 | UI/API | Ready |
| ADMIN-007 | Super Admin | Update SMTP, 2FA and system settings | Settings persist, audit and runtime behaviour are correct | P0 | API/UI | Ready |
| NFR-001 | All key pages | Run keyboard-only navigation and accessible-name checks | Critical flows meet baseline accessibility | P1 | UI | Ready |
| NFR-002 | Mobile/tablet/desktop viewports | Run smoke flows | No clipped controls or unusable interactions | P1 | UI | Ready |
| NFR-003 | Chromium/Firefox/WebKit | Run smoke suite | Critical workflows behave consistently | P1 | UI | Ready |
| NFR-004 | Unauthorised/malformed requests | Fuzz core endpoint permissions and validation | Safe 4xx response; no server error or data exposure | P0 | API | Ready |
| NFR-005 | Concurrent board activity | Create/move/comment from two sessions | No lost updates or incorrect WebSocket state | P1 | UI/API | Ready |
| NFR-006 | Large but permitted data set | Open/filter/search/export board | Response time and UI remain within agreed NFR | P2 | UI/API | Ready |

## Automation implementation order

1. P0 Authentication, board/list/card CRUD, collaboration, permissions and admin access.
2. P0 integrations, payment-webhook safety and system settings.
3. P1 dashboards, search, notifications, exports, templates, subscriptions and browser coverage.
4. P2 performance, responsive, accessibility depth and concurrency.

## Current execution blocker

The application is currently available only on the user's laptop at `http://localhost:5275`, which this environment cannot access. A staging URL or a secure temporary tunnel plus test credentials is required to implement and validate the ready scenarios as executable Playwright tests.


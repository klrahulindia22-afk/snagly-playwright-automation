# Snagly deployed website test coverage

Target: https://snagly.klrahulindia22.workers.dev/

These cases supplement the complete 112-case catalogue in `test-case-catalogue.md`.

| ID | Scenario | Expected result | Priority | Status |
|---|---|---|---|---|
| PUB-001 | Open landing page | Snagly landing page loads without blocking errors | P0 | Ready |
| PUB-002 | Navigate header/footer links | Home, Pricing, Login and Sign-up routes work | P0 | Ready |
| PUB-003 | Use free-account CTA | User reaches sign-up | P0 | Ready |
| PUB-004 | Use pricing CTA | User reaches pricing | P1 | Ready |
| PUB-005 | Interact with landing demo and feature tabs | Cards/tabs render and react correctly | P1 | Ready |
| PUB-006 | Toggle demo filter chips | AND filter, count and clear state work | P1 | Ready |
| PUB-007 | Load pricing plans | Plan cards load; no indefinite loading state | P0 | Ready |
| PUB-008 | Switch monthly/yearly billing | Prices and savings messaging update | P1 | Ready |
| PUB-009 | Expand comparison and FAQs | Content and accessible state toggle correctly | P1 | Ready |
| PUB-010 | Submit empty sign-up form | Required validation appears | P0 | Ready |
| PUB-011 | Submit invalid sign-up values | Email/password/confirmation validation blocks submission | P0 | Ready |
| PUB-012 | Register a unique E2E user | User is created and reaches verification/onboarding | P0 | Blocked |
| PUB-013 | Register an existing email | Safe duplicate-account error appears | P0 | Ready |
| PUB-014 | Follow sign-up login link | Login route loads | P1 | Ready |
| PUB-015 | Use support mail link | Correct mail target is exposed | P2 | Ready |

## Live observation

On 21 Sep 2026, the landing, signup and pricing UI rendered. The pricing page showed **Loading plans…** instead of plan cards; record this as a deployment/API defect until the deployed plans API is available.

Authenticated, integration, payment and destructive scenarios require dedicated E2E users, seeded data, test mailbox access and sandbox-only credentials.

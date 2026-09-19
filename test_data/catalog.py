"""Stable names for the controlled Snagly test database.

These records are created by ``backend/tests/seed.py`` in the Snagly project.
Use the names in UI assertions; IDs are intentionally never hard-coded.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TestUser:
    email: str
    password: str
    role: str


USERS = {
    "admin": TestUser("admin@test.com", "Admin@1234", "super_admin"),
    "owner": TestUser("owner@test.com", "Owner@1234", "owner"),
    "team": TestUser("team@test.com", "Team@1234", "team"),
    "client": TestUser("client@test.com", "Client@1234", "client"),
    "other_owner": TestUser("other@test.com", "Other@1234", "owner"),
}

PRIMARY_BOARD = "Test Board"
ISOLATED_BOARD = "Other Board"
COLUMNS = ("Backlog", "In Progress", "Review", "Done")
LABELS = ("Bug", "UI", "Regression", "Client Reported")

CARDS = {
    "critical_login": "Login page throws 500 on empty password",
    "mobile_drag": "Card drag-and-drop breaks on mobile",
    "email_notifications": "Email notifications not sending",
    "accessibility": "Improve board filter accessibility",
    "csv_export": "CSV export contains duplicate rows",
    "completed_profile": "Profile initials colour is retained",
}

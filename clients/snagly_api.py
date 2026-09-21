"""Small API client for deterministic setup and API assertions.

UI journeys remain the primary coverage. Use this client only to prepare test state
or validate backend responses without relying on browser-only setup steps.
"""

from urllib.parse import urlencode

from playwright.sync_api import APIRequestContext, expect


class SnaglyApi:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self._headers: dict[str, str] = {}

    def login(self, email: str, password: str) -> dict:
        response = self.request.post("/api/v1/auth/login", data={"email": email, "password": password})
        expect(response).to_be_ok()
        body = response.json()["data"]
        if body.get("requires_2fa"):
            raise RuntimeError("The automation account must not have 2FA enabled.")
        self._headers = {"Authorization": f"Bearer {body['access_token']}"}
        return body

    def get_public_plans(self):
        return self.request.get("/api/v1/plans")

    def get_boards(self):
        return self.request.get("/api/v1/boards", headers=self._headers)

    @property
    def headers(self) -> dict[str, str]:
        return dict(self._headers)

    def me(self):
        return self.request.get("/api/v1/users/me", headers=self._headers)

    def create_board(self, name: str, description: str | None = None, bg_color: str = "#006452"):
        return self.request.post("/api/v1/boards", headers=self._headers, data={"name": name, "description": description, "bg_color": bg_color})

    def get_board(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}", headers=self._headers)

    def archive_board(self, board_id: int):
        return self.request.post(f"/api/v1/boards/{board_id}/archive", headers=self._headers)

    def restore_board(self, board_id: int):
        return self.request.post(f"/api/v1/boards/{board_id}/restore", headers=self._headers)

    def delete_board(self, board_id: int):
        return self.request.delete(f"/api/v1/boards/{board_id}", headers=self._headers)

    def get_lists(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/lists", headers=self._headers)

    def create_list(self, board_id: int, name: str):
        return self.request.post(f"/api/v1/boards/{board_id}/lists", headers=self._headers, data={"name": name})

    def create_card(self, board_id: int, list_id: int, title: str, **fields):
        return self.request.post(f"/api/v1/boards/{board_id}/cards", headers=self._headers, data={"list_id": list_id, "title": title, **fields})

    def get_card(self, card_id: int):
        return self.request.get(f"/api/v1/cards/{card_id}", headers=self._headers)

    def update_card(self, card_id: int, **fields):
        return self.request.patch(f"/api/v1/cards/{card_id}", headers=self._headers, data=fields)

    def delete_card(self, card_id: int):
        return self.request.delete(f"/api/v1/cards/{card_id}", headers=self._headers)

    def move_card(self, card_id: int, list_id: int, position: int = 0):
        return self.request.patch(f"/api/v1/cards/{card_id}/move", headers=self._headers, data={"list_id": list_id, "position": position})

    def get_labels(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/labels", headers=self._headers)

    def get_members(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/members", headers=self._headers)

    def get_notifications(self):
        return self.request.get("/api/v1/notifications", headers=self._headers)

    def get_global_dashboard(self):
        return self.request.get("/api/v1/dashboard/global", headers=self._headers)

    def get_board_dashboard(self, board_id: int, days: int = 30):
        return self.request.get(f"/api/v1/boards/{board_id}/dashboard?days={days}", headers=self._headers)

    def search(self, query: str):
        return self.request.get(f"/api/v1/search?{urlencode({'q': query})}", headers=self._headers)

    def get_subscription(self):
        return self.request.get("/api/v1/subscriptions/me", headers=self._headers)

    def get_archived_boards(self):
        return self.request.get("/api/v1/boards/archived", headers=self._headers)

    def get_join_requests(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/join-requests", headers=self._headers)

    def get_board_activity(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/activity", headers=self._headers)

    def get_integrations(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/integrations", headers=self._headers)

    def get_templates(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/templates", headers=self._headers)

    def get_sla_rules(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/sla-rules", headers=self._headers)

    def get_field_definitions(self, board_id: int):
        return self.request.get(f"/api/v1/boards/{board_id}/field-definitions", headers=self._headers)

    def get_notification_preferences(self):
        return self.request.get("/api/v1/users/me/notification-prefs", headers=self._headers)

    def get_digest_preferences(self):
        return self.request.get("/api/v1/users/me/digest-prefs", headers=self._headers)

    def get_invoices(self):
        return self.request.get("/api/v1/invoices", headers=self._headers)

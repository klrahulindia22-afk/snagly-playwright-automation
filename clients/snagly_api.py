"""Small API client for deterministic setup and API assertions.

UI journeys remain the primary coverage. Use this client only to prepare test state
or validate backend responses without relying on browser-only setup steps.
"""

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

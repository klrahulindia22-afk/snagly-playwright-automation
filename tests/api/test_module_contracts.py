import pytest


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(
    "method_name",
    [
        "get_archived_boards",
        "get_notifications",
        "get_notification_preferences",
        "get_digest_preferences",
        "get_subscription",
        "get_invoices",
    ],
)
def test_user_scoped_read_contracts(authenticated_api, method_name):
    response = getattr(authenticated_api, method_name)()
    assert response.status == 200, response.text()
    assert "data" in response.json()


@pytest.mark.api
@pytest.mark.boards
@pytest.mark.parametrize(
    "method_name",
    [
        "get_lists",
        "get_labels",
        "get_members",
        "get_join_requests",
        "get_board_activity",
        "get_integrations",
        "get_templates",
        "get_sla_rules",
        "get_field_definitions",
        "get_board_dashboard",
    ],
)
def test_board_scoped_read_contracts(authenticated_api, disposable_board, method_name):
    response = getattr(authenticated_api, method_name)(disposable_board["id"])
    assert response.status == 200, response.text()
    assert "data" in response.json()


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.parametrize(
    "email,password",
    [
        ("unknown-user@example.com", "WrongPassword1!"),
        ("not-an-email", "WrongPassword1!"),
        ("", ""),
    ],
)
def test_login_rejects_invalid_credentials(api_client, email, password):
    response = api_client.post("/api/v1/auth/login", data={"email": email, "password": password})
    assert response.status in {400, 401, 422}


@pytest.mark.api
@pytest.mark.security
def test_unknown_board_is_not_disclosed(authenticated_api):
    response = authenticated_api.get_board(2_147_483_647)
    assert response.status in {403, 404}

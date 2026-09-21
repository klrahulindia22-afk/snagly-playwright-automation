import pytest


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(
    "method_name",
    [
        pytest.param("get_archived_boards", marks=pytest.mark.case_id("SNAG-TC-044")),
        pytest.param("get_notifications", marks=pytest.mark.case_id("SNAG-TC-122")),
        pytest.param("get_notification_preferences", marks=pytest.mark.case_id("SNAG-TC-121")),
        pytest.param("get_digest_preferences", marks=pytest.mark.case_id("SNAG-TC-127")),
        pytest.param("get_subscription", marks=pytest.mark.case_id("SNAG-TC-035")),
        pytest.param("get_invoices", marks=pytest.mark.case_id("SNAG-TC-031")),
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
        pytest.param("get_lists", marks=pytest.mark.case_id("SNAG-TC-047")),
        pytest.param("get_labels", marks=pytest.mark.case_id("SNAG-TC-067")),
        pytest.param("get_members", marks=pytest.mark.case_id("SNAG-TC-106")),
        pytest.param("get_join_requests", marks=pytest.mark.case_id("SNAG-TC-104")),
        pytest.param("get_board_activity", marks=pytest.mark.case_id("SNAG-TC-064")),
        pytest.param("get_integrations", marks=pytest.mark.case_id("SNAG-TC-134")),
        pytest.param("get_templates", marks=pytest.mark.case_id("SNAG-TC-056")),
        pytest.param("get_sla_rules", marks=pytest.mark.case_id("SNAG-TC-069")),
        pytest.param("get_field_definitions", marks=pytest.mark.case_id("SNAG-TC-060")),
        pytest.param("get_board_dashboard", marks=pytest.mark.case_id("SNAG-TC-108")),
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
        pytest.param(
            "unknown-user@example.com",
            "WrongPassword1!",
            marks=pytest.mark.case_id("SNAG-TC-011"),
        ),
        pytest.param(
            "not-an-email",
            "WrongPassword1!",
            marks=pytest.mark.case_id("SNAG-TC-013"),
        ),
        pytest.param("", "", marks=pytest.mark.case_id("SNAG-TC-012")),
    ],
)
def test_login_rejects_invalid_credentials(api_client, email, password):
    response = api_client.post("/api/v1/auth/login", data={"email": email, "password": password})
    assert response.status in {400, 401, 422}


@pytest.mark.api
@pytest.mark.security
@pytest.mark.case_id("SNAG-TC-140")
def test_unknown_board_is_not_disclosed(authenticated_api):
    response = authenticated_api.get_board(2_147_483_647)
    assert response.status in {403, 404}

import pytest

from utils.contracts import assert_collection, assert_envelope


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.case_id("SNAG-TC-016")
def test_current_user_contract(authenticated_api):
    user = assert_envelope(authenticated_api.me(), schema="user")
    assert {"id", "email", "full_name", "role"}.issubset(user)


@pytest.mark.api
@pytest.mark.boards
@pytest.mark.case_id("SNAG-TC-037")
def test_boards_contract(authenticated_api):
    boards = assert_collection(authenticated_api.get_boards(), schema="board-list")
    for board in boards:
        assert {"id", "name", "slug", "my_role", "member_count"}.issubset(board)


@pytest.mark.api
@pytest.mark.boards
@pytest.mark.case_id("SNAG-TC-055")
def test_board_list_card_crud(authenticated_api, disposable_board, disposable_list, disposable_card):
    assert assert_envelope(authenticated_api.get_board(disposable_board["id"]))["id"] == disposable_board["id"]
    assert disposable_list["id"] in {item["id"] for item in assert_collection(authenticated_api.get_lists(disposable_board["id"]))}
    assert assert_envelope(authenticated_api.get_card(disposable_card["id"]))["title"] == disposable_card["title"]


@pytest.mark.api
@pytest.mark.cards
@pytest.mark.case_id("SNAG-TC-060")
def test_card_update_contract(authenticated_api, disposable_card):
    updated = assert_envelope(authenticated_api.update_card(disposable_card["id"], priority="high"))
    assert updated["priority"] == "high"


@pytest.mark.api
@pytest.mark.reports
@pytest.mark.case_id("SNAG-TC-116")
def test_global_dashboard_contract(authenticated_api):
    response = authenticated_api.get_global_dashboard()
    assert response.status == 200, response.text()
    assert "data" in response.json()


@pytest.mark.api
@pytest.mark.notifications
@pytest.mark.case_id("SNAG-TC-122")
def test_notifications_contract(authenticated_api):
    response = authenticated_api.get_notifications()
    assert response.status == 200, response.text()
    assert "data" in response.json()


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.case_id("SNAG-TC-082")
def test_search_contract(authenticated_api):
    response = authenticated_api.search("E2E")
    assert response.status == 200, response.text()
    assert "data" in response.json()


@pytest.mark.api
@pytest.mark.security
@pytest.mark.case_id("SNAG-TC-017")
def test_protected_endpoint_rejects_anonymous(api_client):
    response = api_client.get("/api/v1/boards")
    assert response.status in {401, 403}

import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.boards
@pytest.mark.case_id("SNAG-TC-037")
def test_authenticated_user_can_open_boards(authenticated_page):
    expect(authenticated_page).to_have_url("**/boards")
    expect(authenticated_page.get_by_role("button", name="Boards", exact=True)).to_be_visible()

import pytest
from playwright.sync_api import expect

from pages.board_page import BoardPage
from pages.boards_page import BoardsPage


@pytest.mark.boards
@pytest.mark.smoke
def test_boards_dashboard_controls(authenticated_page, app_url):
    boards = BoardsPage(authenticated_page, app_url)
    boards.open()
    expect(boards.new_board.first).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Active")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Archived")).to_be_visible()


@pytest.mark.boards
@pytest.mark.regression
def test_board_displays_default_workflow(authenticated_page, app_url, disposable_board):
    board = BoardPage(authenticated_page, app_url)
    board.open_by_id(disposable_board["id"])
    for name in ("Share", "Filters", "Reports", "Archive"):
        expect(authenticated_page.get_by_role("button", name=name, exact=True)).to_be_visible()


@pytest.mark.boards
@pytest.mark.cards
@pytest.mark.regression
def test_api_seeded_card_is_visible(authenticated_page, app_url, disposable_board, disposable_card):
    board = BoardPage(authenticated_page, app_url)
    board.open_by_id(disposable_board["id"])
    expect(authenticated_page.get_by_text(disposable_card["title"], exact=True)).to_be_visible()


@pytest.mark.boards
@pytest.mark.regression
def test_filter_panel_lists_supported_filters(authenticated_page, app_url, disposable_board):
    board = BoardPage(authenticated_page, app_url)
    board.open_by_id(disposable_board["id"])
    board.open_filters()
    for label in ("Priority", "Severity", "Source", "Due Date", "Column"):
        expect(authenticated_page.get_by_text(label, exact=True)).to_be_visible()


@pytest.mark.boards
@pytest.mark.permissions
def test_share_dialog_exposes_team_and_client_roles(authenticated_page, app_url, disposable_board):
    board = BoardPage(authenticated_page, app_url)
    board.open_by_id(disposable_board["id"])
    board.open_share()
    role = authenticated_page.locator("select").last
    expect(role.locator("option", has_text="Team")).to_have_count(1)
    expect(role.locator("option", has_text="Client")).to_have_count(1)

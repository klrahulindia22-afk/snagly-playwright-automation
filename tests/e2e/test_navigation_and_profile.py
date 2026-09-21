import pytest
from playwright.sync_api import expect

from pages.app_pages import GlobalNav, NotificationsPage, ProfilePage, ReportsPage


@pytest.mark.regression
@pytest.mark.case_id("SNAG-TC-088")
def test_global_search_opens(authenticated_page):
    nav = GlobalNav(authenticated_page)
    nav.open_search()
    expect(authenticated_page.get_by_placeholder("Search cards across all boards…")).to_be_focused()


@pytest.mark.profile
@pytest.mark.regression
@pytest.mark.case_id("SNAG-TC-125")
def test_profile_page_loads(authenticated_page, app_url):
    ProfilePage(authenticated_page, app_url).open()
    expect(authenticated_page.get_by_text("Identity", exact=True)).to_be_visible()


@pytest.mark.notifications
@pytest.mark.regression
@pytest.mark.case_id("SNAG-TC-122")
def test_notifications_route_loads(authenticated_page, app_url):
    NotificationsPage(authenticated_page, app_url).open()
    expect(authenticated_page).to_have_url("**/notifications")


@pytest.mark.reports
@pytest.mark.regression
@pytest.mark.case_id("SNAG-TC-116")
def test_global_reports_route_loads(authenticated_page, app_url):
    ReportsPage(authenticated_page, app_url).open_global()
    expect(authenticated_page).to_have_url("**/reports")


@pytest.mark.regression
@pytest.mark.case_id("SNAG-TC-128")
def test_theme_toggle_changes_document_theme(authenticated_page):
    nav = GlobalNav(authenticated_page)
    before = authenticated_page.locator("html").get_attribute("class") or ""
    nav.toggle_theme()
    after = authenticated_page.locator("html").get_attribute("class") or ""
    assert before != after


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.case_id("SNAG-TC-018")
def test_sign_out_clears_access(authenticated_page):
    GlobalNav(authenticated_page).sign_out()
    expect(authenticated_page).to_have_url("**/login")
    authenticated_page.goto("/boards")
    expect(authenticated_page).to_have_url("**/login")

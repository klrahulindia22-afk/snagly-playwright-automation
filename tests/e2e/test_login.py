import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.auth
def test_login_page_loads(page, app_url):
    login = LoginPage(page, app_url)
    login.open()

    expect(login.email).to_be_visible()
    expect(login.password).to_be_visible()
    expect(login.submit).to_be_enabled()


@pytest.mark.smoke
@pytest.mark.auth
def test_login_requires_email_and_password(page, app_url):
    login = LoginPage(page, app_url)
    login.open()
    login.submit.click()

    expect(page.get_by_text("Email address is required.")).to_be_visible()
    expect(page.get_by_text("Password is required.")).to_be_visible()


@pytest.mark.smoke
@pytest.mark.auth
def test_user_can_log_in(authenticated_page):
    expect(authenticated_page).to_have_url("**/boards")

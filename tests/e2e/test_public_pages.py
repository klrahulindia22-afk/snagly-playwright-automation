import re

import pytest
from playwright.sync_api import expect

from pages.public_pages import ForgotPasswordPage, LandingPage, PricingPage, SignupPage
from utils.accessibility import assert_no_horizontal_overflow


@pytest.mark.public
@pytest.mark.smoke
@pytest.mark.case_id("SNAG-TC-001")
def test_landing_page_core_navigation(page, app_url, case_data):
    assert case_data.module == "Landing Page"
    landing = LandingPage(page, app_url)
    landing.open()
    expect(page.get_by_role("link", name="Pricing").first).to_be_visible()
    expect(page.get_by_role("link", name=re.compile(r"Start free")).first).to_be_visible()


@pytest.mark.public
@pytest.mark.regression
def test_pricing_lists_all_plans(page, app_url):
    pricing = PricingPage(page, app_url)
    pricing.open()
    for plan in ("Free", "Pro", "Business", "Enterprise"):
        expect(page.get_by_text(plan, exact=True).first).to_be_visible()


@pytest.mark.public
@pytest.mark.auth
def test_signup_form_fields(page, app_url):
    signup = SignupPage(page, app_url)
    signup.open()
    expect(signup.name).to_be_visible()
    expect(signup.email).to_be_visible()
    expect(signup.password).to_be_visible()
    expect(signup.confirm).to_be_visible()


@pytest.mark.public
@pytest.mark.auth
def test_forgot_password_form(page, app_url):
    forgot = ForgotPasswordPage(page, app_url)
    forgot.open()
    expect(page.get_by_role("button", name="Send reset link")).to_be_visible()


@pytest.mark.public
@pytest.mark.responsive
@pytest.mark.parametrize("width,height", [(320, 568), (375, 812), (768, 1024), (1440, 900)])
def test_landing_page_reflows(page, app_url, width, height):
    page.set_viewport_size({"width": width, "height": height})
    LandingPage(page, app_url).open()
    assert_no_horizontal_overflow(page)

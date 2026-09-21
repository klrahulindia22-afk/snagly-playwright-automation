import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LandingPage(BasePage):
    def open(self) -> None:
        self.goto("/")
        expect(self.page.get_by_role("heading", name="Bug tracking that clients actually understand")).to_be_visible()


class PricingPage(BasePage):
    def open(self) -> None:
        self.goto("/pricing")
        expect(self.page.get_by_role("heading", name="Simple, honest pricing")).to_be_visible()

    def select_yearly(self) -> None:
        self.page.get_by_role("button", name=re.compile(r"^Yearly")).click()


class SignupPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.name = page.get_by_placeholder("Your full name")
        self.email = page.get_by_placeholder("you@company.com")
        self.password = page.get_by_placeholder("Create a strong password")
        self.confirm = page.get_by_placeholder("Repeat your password")
        self.submit = page.get_by_role("button", name="Create account")

    def open(self) -> None:
        self.goto("/signup")
        expect(self.page.get_by_text("Create your account")).to_be_visible()


class ForgotPasswordPage(BasePage):
    def open(self) -> None:
        self.goto("/forgot-password")
        expect(self.page.get_by_text("Reset your password")).to_be_visible()

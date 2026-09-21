import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class GlobalNav:
    def __init__(self, page: Page):
        self.page = page

    def open_search(self) -> None:
        self.page.get_by_role("button", name="Search").click()

    def search(self, text: str) -> None:
        self.open_search()
        self.page.get_by_placeholder("Search cards across all boards…").fill(text)

    def toggle_theme(self) -> None:
        self.page.get_by_role("button", name=re.compile(r"mode", re.I)).click()

    def sign_out(self) -> None:
        self.page.get_by_role("button", name="Sign out").click()


class ReportsPage(BasePage):
    def open_global(self) -> None:
        self.goto("/reports")
        self.page.wait_for_load_state("domcontentloaded")

    def select_period(self, days: int) -> None:
        self.page.get_by_role("button", name=f"{days}d").click()

    def export_csv(self):
        with self.page.expect_download() as download:
            self.page.get_by_role("button", name=re.compile(r"CSV")).click()
        return download.value


class ProfilePage(BasePage):
    def open(self) -> None:
        self.goto("/profile")
        expect(self.page.get_by_text("Profile", exact=True)).to_be_visible()

    def update_name(self, name: str) -> None:
        self.page.get_by_label("Full name").fill(name)
        self.page.get_by_role("button", name=re.compile(r"Save")).first.click()


class NotificationsPage(BasePage):
    def open(self) -> None:
        self.goto("/notifications")
        expect(self.page).to_have_url("**/notifications")

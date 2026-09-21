import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class BoardPage(BasePage):
    def open_by_id(self, board_id: int) -> None:
        self.goto(f"/board/{board_id}")
        expect(self.page.get_by_role("button", name="Filters")).to_be_visible()

    def open_filters(self) -> None:
        self.page.get_by_role("button", name="Filters").click()
        expect(self.page.get_by_role("heading", name="Filter cards")).to_be_visible()

    def apply_filter(self, name: str) -> None:
        self.open_filters()
        self.page.get_by_role("button", name=name, exact=True).first.click()

    def open_share(self) -> None:
        self.page.get_by_role("button", name="Share").click()
        expect(self.page.get_by_role("heading", name="Share Board")).to_be_visible()

    def start_card(self, list_name: str = "Backlog") -> None:
        column = self.page.get_by_role("button", name=re.compile(rf"^{re.escape(list_name)} List actions"))
        column.locator("xpath=following-sibling::*").get_by_role("button", name="Add a card").click()

    def create_card(self, title: str, description: str = "", priority: str = "Normal", severity: str = "No severity") -> None:
        self.page.get_by_role("button", name="Add a card").first.click()
        self.page.get_by_placeholder("Enter card title…").fill(title)
        if description:
            self.page.get_by_placeholder("Add a description…").fill(description)
        self.page.get_by_label("Priority").select_option(label=priority)
        self.page.get_by_label("Severity").select_option(label=severity)
        self.page.get_by_role("button", name="Create card").click()
        expect(self.page.get_by_text(title, exact=True)).to_be_visible()

    def open_card(self, title: str) -> None:
        self.page.get_by_text(title, exact=True).click()

    def open_reports(self) -> None:
        self.page.get_by_role("button", name="Reports", exact=True).click()
        self.page.wait_for_url("**/reports")

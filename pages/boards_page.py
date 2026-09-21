import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class BoardsPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.new_board = page.get_by_role("button", name=re.compile(r"^\+ New [Bb]oard$"))

    def open(self) -> None:
        self.goto("/boards")
        expect(self.page.get_by_role("button", name="Boards", exact=True)).to_be_visible()

    def open_board(self, name: str) -> None:
        self.page.get_by_role("button", name=re.compile(re.escape(name))).click()
        self.page.wait_for_url("**/board/*")

    def switch_to_archived(self) -> None:
        self.page.get_by_role("button", name="Archived", exact=True).click()

    def start_create_board(self) -> None:
        self.new_board.first.click()

    def create_board(self, name: str, description: str = "") -> None:
        self.start_create_board()
        self.page.get_by_placeholder("e.g. Mobile App Bugs").fill(name)
        if description:
            self.page.get_by_placeholder("What's this board for?").fill(description)
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name=re.compile(r"Create|Finish")).click()
        expect(self.page).to_have_url("**/board/*")

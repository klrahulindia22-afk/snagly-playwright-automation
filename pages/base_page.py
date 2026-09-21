from pathlib import Path

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, path: str = "") -> None:
        self.page.goto(f"{self.base_url}{path}", wait_until="domcontentloaded")

    def expect_path(self, pattern: str) -> None:
        expect(self.page).to_have_url(pattern)

    def dismiss_dialog(self) -> None:
        self.page.keyboard.press("Escape")

    def save_screenshot(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path), full_page=True)

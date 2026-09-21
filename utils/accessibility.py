from playwright.sync_api import Page


def assert_basic_accessibility(page: Page) -> None:
    violations = page.locator("button:not([aria-label]):not(:has-text(*)), a:not([aria-label]):not(:has-text(*)), input:not([aria-label]):not([placeholder]):not([type=hidden])").count()
    assert violations == 0, f"Found {violations} interactive elements without an accessible name"


def assert_no_horizontal_overflow(page: Page) -> None:
    overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
    assert not overflow, "Page has unexpected horizontal overflow"

from playwright.sync_api import Page, expect


class LoginPage:
    """Interactions for Snagly's /login screen."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.url = f"{base_url}/login"
        self.email = page.locator('input[type="email"]')
        self.password = page.locator('input[type="password"]')
        self.submit = page.get_by_role("button", name="Log in")

    def open(self) -> None:
        self.page.goto(self.url, wait_until="domcontentloaded")
        expect(self.page.get_by_text("Sign in to your workspace")).to_be_visible()

    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

    def expect_authenticated(self) -> None:
        self.page.wait_for_url("**/boards", timeout=15_000)
        expect(self.page).to_have_url("**/boards")

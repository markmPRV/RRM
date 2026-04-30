import uuid

from playwright.sync_api import Page


def login(
    page: Page,
    user: str,
    password: str,
    timeout: int = 60000) -> Page:
    """
    Log in to the website with resilient waiting.
    """
    print(f"Logging In as `{user}`...")
    page.get_by_role("link", name="Log in").click()
    page.locator("#loginusername").fill(user)
    page.locator("#loginpassword").fill(password)
    page.get_by_role("button", name="Log in").click()

    return page


def generate_key():
    return f"key_{uuid.uuid4().hex[:6]}"


def get_products(page: Page):
    products = page.locator("#tbodyid > div.col-lg-4")
    products.first.wait_for(state="visible")

    return products

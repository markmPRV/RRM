from playwright.sync_api import Page, expect

from utils.constants import BASE_URL, VALID_USER
from infra import helpers as h


def test_successful_login(page: Page):
    """
    Test successful Login process
    :param page:
    :param browser_name:
    """
    page.goto(BASE_URL)

    h.login(page, VALID_USER["username"], VALID_USER["password"])

    expect(
        page.get_by_role("link", name=f"Welcome {VALID_USER["username"]}"),
        f"Validation for Welcome message failed"
    ).to_be_visible()


def test_invalid_user(page: Page):
    """
    Test invalid User in the Login process
    :param page:
    :param browser_name:
    """
    page.goto(BASE_URL)
    random_user = h.generate_key()

    with page.expect_event("dialog") as dialog_info:
        h.login(page, random_user, VALID_USER["password"])

    dialog = dialog_info.value

    assert "User does not exist" in dialog.message
    dialog.accept()


def test_invalid_password(page: Page):
    """
    Test invalid Password in the Login process
    :param page:
    :param browser_name:
    """
    page.goto(BASE_URL)
    random_pass = h.generate_key()

    with page.expect_event("dialog") as dialog_info:
        h.login(page, VALID_USER["username"], random_pass)

    dialog = dialog_info.value

    assert "Wrong password" in dialog.message
    dialog.accept()


def test_logout(page: Page):
    """
    Test Logout process
    :param page:
    :param browser_name:
    """
    page.goto(BASE_URL)

    h.login(page, VALID_USER["username"], VALID_USER["password"])

    expect(
        page.get_by_role("link", name=f"Welcome {VALID_USER["username"]}"),
        f"Validation for Welcome message failed"
    ).to_be_visible()

    page.get_by_role("link", name="Log out").click()

    expect(
        page.get_by_role("link", name=f"Welcome {VALID_USER["username"]}"),
        f"Still logged in"
    ).not_to_be_visible()

    expect(page.get_by_role("link", name="Log in")).to_be_visible()

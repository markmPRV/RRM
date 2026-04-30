from playwright.sync_api import Page, expect

from utils.constants import BASE_URL, PURCHASE_DATA


def test_purchase(page: Page):
    """
    Test that operates on a cart, add and delete items, and purchase the products at the end.
    :param page: 
    :return:
    """
    page.goto(BASE_URL)

    # Dialog handler
    messages = []

    def handle_dialog(dialog):
        messages.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)

    # Add first product to the cart
    page.get_by_role("link", name="Samsung galaxy s6").click()
    page.get_by_role("link", name="Add to cart").click()

    # Verify the cart
    page.get_by_role("link", name="Cart", exact=True).click()
    expect(page.get_by_role("columnheader", name="Pic")).to_be_visible()
    expect(page.get_by_role("columnheader", name="Title")).to_be_visible()
    expect(page.get_by_role("columnheader", name="Price")).to_be_visible()
    expect(page.get_by_role("columnheader", name="x")).to_be_visible()
    expect(page.get_by_role("cell", name="Samsung galaxy s6")).to_be_visible()
    expect(page.get_by_role("heading", name="Total")).to_be_visible()
    expect(page.get_by_role("heading", name="360")).to_be_visible()
    expect(page.get_by_role("button", name="Place Order")).to_be_visible()
    expect(page.get_by_role("link", name="Delete")).to_be_visible()

    # Add second product to the cart
    page.get_by_role("link", name="Home (current)").click()
    page.get_by_role("link", name="Sony vaio i5").click()
    page.get_by_role("link", name="Add to cart").click()

    # Add third product to the cart
    page.get_by_role("link", name="Home (current)").click()
    page.get_by_role("link", name="HTC One M9").click()
    page.get_by_role("link", name="Add to cart").click()

    # Verify the cart
    page.get_by_role("link", name="Cart", exact=True).click()
    expect(page.get_by_role("cell", name="Samsung galaxy s6")).to_be_visible()
    expect(page.get_by_role("cell", name="Sony vaio i5")).to_be_visible()
    expect(page.get_by_role("cell", name="HTC One M9")).to_be_visible()
    expect(page.get_by_role("heading", name="Total")).to_be_visible()
    expect(page.get_by_role("heading", name="1850")).to_be_visible()

    # Delete the HTC from the cart and verify the content of the cart
    page.locator("#tbodyid tr", has_text="HTC").get_by_role("link", name="Delete").click()
    expect(page.get_by_role("cell", name="Samsung galaxy s6")).to_be_visible()
    expect(page.get_by_role("cell", name="Sony vaio i5")).to_be_visible()
    expect(page.get_by_role("cell", name="HTC One M9")).not_to_be_visible()
    expect(page.get_by_role("heading", name="Total")).to_be_visible()
    expect(page.get_by_role("heading", name="1150")).to_be_visible()
    expect(page.get_by_role("button", name="Place Order")).to_be_visible()

    # Place an order
    page.get_by_role("button", name="Place Order").click()
    expect(page.get_by_role("button", name="Purchase")).to_be_visible()
    expect(page.get_by_label("Place order").get_by_text("Close")).to_be_visible()

    # Verify no order can be placed if Name and Card number are NOT provided
    page.get_by_role("button", name="Purchase").click()
    print(f"Messages: {messages}")
    assert messages[-1] == "Please fill out Name and Creditcard."

    # Fill all the fields and verify successful purchase
    page.get_by_role("textbox", name="Total: 1150 Name:").fill(PURCHASE_DATA["name"])
    page.get_by_role("textbox", name="Country:").fill(PURCHASE_DATA["country"])
    page.get_by_role("textbox", name="City:").fill(PURCHASE_DATA["city"])
    page.get_by_role("textbox", name="Credit card:").fill(PURCHASE_DATA["card"])
    page.get_by_role("textbox", name="Month:").fill(PURCHASE_DATA["month"])
    page.get_by_role("textbox", name="Year:").fill(PURCHASE_DATA["year"])
    page.get_by_role("button", name="Purchase").click()
    expect(page.get_by_role("heading", name="Thank you for your purchase!")).to_be_visible()
    expect(page.get_by_role("button", name="OK")).to_be_visible()
    page.get_by_role("button", name="OK").click()

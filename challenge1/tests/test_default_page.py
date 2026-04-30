import pytest
from playwright.sync_api import Page, expect

from utils.constants import BASE_URL, CATEGORIES
from infra import helpers as h


def test_default_content(page: Page):
    """
    Test existence of default page content: Links, buttons and more.
    """
    page.goto(BASE_URL)

    expect(page.get_by_role("link", name="Home (current)")).to_be_visible()
    expect(page.get_by_role("link", name="Contact")).to_be_visible()
    expect(page.get_by_role("link", name="About us")).to_be_visible()
    expect(page.get_by_role("link", name="Cart")).to_be_visible()
    expect(page.get_by_role("link", name="Log in")).to_be_visible()
    expect(page.get_by_role("link", name="Sign up")).to_be_visible()
    expect(page.get_by_role("link", name="PRODUCT STORE")).to_be_visible()
    expect(page.locator("#carouselExampleIndicators").get_by_role("button", name="Previous")).to_be_visible()
    expect(page.locator("#carouselExampleIndicators").get_by_role("button", name="Next")).to_be_visible()
    expect(page.get_by_role("link", name="CATEGORIES")).to_be_visible()
    for category in CATEGORIES:
        print(f"Category {category}")
        expect(page.get_by_role("link", name=category)).to_be_visible()
    expect(page.locator("#next2")).to_be_visible()
    expect(page.locator("#prev2")).to_be_visible()
    expect(page.get_by_text("About Us", exact=True)).to_be_visible()
    expect(page.get_by_text("Get in Touch")).to_be_visible()
    expect(page.get_by_text("Address: 2390 El Camino Real")).to_be_visible()


def test_count_products(page: Page):
    """
    Validate the count of products per page
    """
    page.goto(BASE_URL)

    products = h.get_products(page)
    count = products.count()
    print("Product count:", count)

    assert count == 9, "Count should be 9"

    page.locator("#next2").click()
    expect(page.get_by_role("link", name="Apple monitor")).to_be_visible()

    count = products.count()
    print("Product count:", count)

    assert count == 6, "Count should be 6"


@pytest.mark.parametrize("category", CATEGORIES)
def test_category_products(page: Page, category: str):
    """
    Validate the count of products as per category
    """
    page.goto(BASE_URL)
    expected_counts = {
        CATEGORIES[0]: 7,
        CATEGORIES[1]: 6,
        CATEGORIES[2]: 2,
    }

    page.get_by_role("link", name=category).click()

    products = h.get_products(page)

    expect(
        products,
        f"{category} should display {expected_counts[category]} products"
    ).to_have_count(expected_counts[category])

    count = products.count()
    print("Product count:", count)
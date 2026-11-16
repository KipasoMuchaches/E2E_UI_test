"""E2E-тесты для SauceDemo (https://www.saucedemo.com/): вход, корзина, оформление заказа."""
import re

import pytest
from playwright.sync_api import Page, expect

USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCT_NAME = "Sauce Labs Backpack"
PRODUCT_ID = "sauce-labs-backpack"

CUSTOMER = {
    "first_name": "Murad",
    "last_name": "Azizov",
    "postal_code": "12345",
}


def login(page: Page, username: str = USERNAME, password: str = PASSWORD) -> None:
    page.goto("/")
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))


def test_checkout_single_product(page: Page) -> None:
    # Авторизация
    login(page)

    # Выбор товара и переход в корзину
    page.click(f"#add-to-cart-{PRODUCT_ID}")
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    page.click(".shopping_cart_link")
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".cart_item")).to_have_count(1)
    expect(page.locator(".cart_item .inventory_item_name")).to_have_text(PRODUCT_NAME)

    # Оформление заказа: данные покупателя
    page.click("#checkout")
    page.fill("#first-name", CUSTOMER["first_name"])
    page.fill("#last-name", CUSTOMER["last_name"])
    page.fill("#postal-code", CUSTOMER["postal_code"])
    page.click("#continue")

    # Проверка сводки заказа и завершение покупки
    expect(page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
    expect(page.locator(".cart_item .inventory_item_name")).to_have_text(PRODUCT_NAME)
    page.click("#finish")

    # Сообщение об успешном заказе
    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")


@pytest.mark.parametrize(
    ("username", "password", "error"),
    [
        ("standard_user", "wrong_password", "Username and password do not match any user in this service"),
        ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
        ("", PASSWORD, "Username is required"),
        (USERNAME, "", "Password is required"),
    ],
    ids=["wrong-password", "locked-out-user", "empty-username", "empty-password"],
)
def test_login_errors(page: Page, username: str, password: str, error: str) -> None:
    page.goto("/")
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")

    expect(page.locator('[data-test="error"]')).to_contain_text(error)
    expect(page).not_to_have_url(re.compile(r"/inventory\.html$"))


def test_remove_product_from_cart(page: Page) -> None:
    login(page)
    page.click(f"#add-to-cart-{PRODUCT_ID}")
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    page.click(".shopping_cart_link")
    expect(page.locator(".cart_item")).to_have_count(1)
    page.click(f"#remove-{PRODUCT_ID}")

    expect(page.locator(".cart_item")).to_have_count(0)
    expect(page.locator(".shopping_cart_badge")).to_have_count(0)


@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "error"),
    [
        ("", CUSTOMER["last_name"], CUSTOMER["postal_code"], "First Name is required"),
        (CUSTOMER["first_name"], "", CUSTOMER["postal_code"], "Last Name is required"),
        (CUSTOMER["first_name"], CUSTOMER["last_name"], "", "Postal Code is required"),
    ],
    ids=["empty-first-name", "empty-last-name", "empty-postal-code"],
)
def test_checkout_required_fields(
    page: Page, first_name: str, last_name: str, postal_code: str, error: str
) -> None:
    login(page)
    page.click(f"#add-to-cart-{PRODUCT_ID}")
    page.click(".shopping_cart_link")
    page.click("#checkout")

    page.fill("#first-name", first_name)
    page.fill("#last-name", last_name)
    page.fill("#postal-code", postal_code)
    page.click("#continue")

    expect(page.locator('[data-test="error"]')).to_contain_text(error)
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))

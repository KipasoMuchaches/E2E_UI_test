"""E2E-тест оформления заказа на SauceDemo (https://www.saucedemo.com/)."""
import re

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

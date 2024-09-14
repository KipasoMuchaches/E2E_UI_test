import time
from playwright.sync_api import sync_playwright


def sync_work():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com/") # Переход на сайт
        # Авторизация
        page.fill('#user-name', 'standard_user') # Логин
        page.fill('#password', 'secret_sauce') # Пароль
        page.click('#login-button')

        page.click('#add-to-cart-sauce-labs-backpack') # Выбор товара
        page.click('.shopping_cart_link') # Переход в корзину
        assert 'Sauce Labs Backpack' in page.inner_text('.cart_item') # Проверка на наличее выбранного товара в корзине

        page.click('#checkout') # Переход на оформление
        page.fill('#first-name', 'Murad') # Имя
        page.fill('#last-name', 'Azizov') # Фамилия
        page.fill('#postal-code', '12345') # Кол
        page.click('#continue')
        page.click('#finish') # Завершить покупку

        page.wait_for_selector('.complete-header') # Ожидание появления сообщения о том что все успешно
        message = page.inner_text('.complete-header').strip()
        print(f'Message: {message}') # Вывод сообщения в консоль о том что успешно

        print('Тест успешно завершен')

        time.sleep(5) # Задержка перед закрытием браузера
        browser.close()

sync_work()


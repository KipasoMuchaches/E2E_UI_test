# E2E UI тест для SauceDemo

Этот проект содержит E2E-тест, который моделирует покупку товара на сайте [SauceDemo](https://www.saucedemo.com/). Тест написан на Python с использованием [Playwright](https://playwright.dev/python/) и [pytest](https://docs.pytest.org/) и проходит весь путь от авторизации до успешного завершения заказа.

## Структура проекта

- `test_playwright.py` — сценарий E2E-теста.
- `conftest.py` — общие фикстуры pytest (опциональная настройка пути к браузеру).
- `pytest.ini` — настройки pytest (базовый URL сайта).
- `requirements.txt` — зависимости проекта.
- `README.md` — документация по настройке и запуску.

## Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/KipasoMuchaches/E2E_UI_test.git
cd E2E_UI_test
```

### 2. Установите зависимости

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Запуск

По умолчанию тест работает в headless-режиме (без окна браузера), поэтому подходит для CI:

```bash
pytest
```

Полезные опции `pytest-playwright`:

```bash
pytest --headed                   # показать окно браузера
pytest --headed --slowmo 500      # замедлить действия, чтобы было видно шаги
pytest --browser firefox          # запустить в другом браузере
pytest --screenshot only-on-failure --video retain-on-failure   # артефакты при падении (в test-results/)
```

Если `playwright install` недоступен (например, в контейнере с уже установленным Chromium), укажите путь к браузеру через переменную окружения:

```bash
CHROMIUM_EXECUTABLE_PATH=/path/to/chrome pytest
```

## Сценарий теста

1. **Авторизация** с тестовыми учётными данными:
   - имя пользователя: `standard_user`
   - пароль: `secret_sauce`
2. **Выбор товара:** добавляет «Sauce Labs Backpack» в корзину и проверяет счётчик корзины.
3. **Корзина:** проверяет, что в корзине ровно один товар с нужным названием.
4. **Оформление заказа:** заполняет имя, фамилию и почтовый индекс и проверяет товар на странице сводки.
5. **Завершение покупки:** завершает заказ и проверяет сообщение «Thank you for your order!».

Каждый шаг проверяется через `expect` из Playwright: проверки автоматически ждут появления нужного состояния, поэтому фиксированные задержки (`time.sleep`) не нужны.

## Настройка

Товар, учётные данные и данные покупателя вынесены в константы в начале `test_playwright.py` (`PRODUCT_NAME`, `PRODUCT_ID`, `USERNAME`, `PASSWORD`, `CUSTOMER`). Чтобы протестировать другой товар, поменяйте их значения.

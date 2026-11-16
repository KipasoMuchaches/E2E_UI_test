# E2E UI тесты для SauceDemo

Этот проект содержит E2E-тесты, которые моделируют покупку товара на сайте [SauceDemo](https://www.saucedemo.com/). Тесты написаны на Python с использованием [Playwright](https://playwright.dev/python/) и [pytest](https://docs.pytest.org/): основной сценарий проходит весь путь от авторизации до успешного завершения заказа, остальные проверяют ошибки и граничные случаи.

## Структура проекта

- `test_playwright.py` — E2E-тесты.
- `conftest.py` — общие фикстуры pytest (опциональная настройка пути к браузеру).
- `pytest.ini` — настройки pytest (базовый URL сайта).
- `requirements.txt` — зависимости проекта.
- `.github/workflows/e2e.yml` — запуск тестов в GitHub Actions.
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

По умолчанию тесты работают в headless-режиме (без окна браузера), поэтому подходят для CI:

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

## Тесты

### `test_checkout_single_product` — покупка товара

1. **Авторизация** с тестовыми учётными данными:
   - имя пользователя: `standard_user`
   - пароль: `secret_sauce`
2. **Выбор товара:** добавляет «Sauce Labs Backpack» в корзину и проверяет счётчик корзины.
3. **Корзина:** проверяет, что в корзине ровно один товар с нужным названием.
4. **Оформление заказа:** заполняет имя, фамилию и почтовый индекс и проверяет товар на странице сводки.
5. **Завершение покупки:** завершает заказ и проверяет сообщение «Thank you for your order!».

### `test_login_errors` — ошибки входа

Неверный пароль, заблокированный пользователь `locked_out_user`, пустой логин и пустой пароль. Для каждого случая проверяется текст ошибки и то, что вход не выполнен.

### `test_remove_product_from_cart` — удаление из корзины

Добавляет товар, удаляет его на странице корзины и проверяет, что корзина пуста и счётчик исчез.

### `test_checkout_required_fields` — обязательные поля при оформлении

По очереди оставляет пустым имя, фамилию и почтовый индекс и проверяет сообщение об ошибке и то, что оформление не продвинулось дальше.

Каждый шаг проверяется через `expect` из Playwright: проверки автоматически ждут появления нужного состояния, поэтому фиксированные задержки (`time.sleep`) не нужны.

## CI

Тесты автоматически запускаются в GitHub Actions на каждый пуш в `main` и на каждый pull request; их также можно запустить вручную на вкладке **Actions**. При падении скриншоты и видео сохраняются как артефакт `playwright-test-results`.

## Настройка

Товар, учётные данные и данные покупателя вынесены в константы в начале `test_playwright.py` (`PRODUCT_NAME`, `PRODUCT_ID`, `USERNAME`, `PASSWORD`, `CUSTOMER`). Чтобы протестировать другой товар, поменяйте их значения.

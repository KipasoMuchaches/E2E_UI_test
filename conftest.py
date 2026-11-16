import os

import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Позволяет указать свой бинарник браузера через CHROMIUM_EXECUTABLE_PATH.

    Полезно в CI/контейнерах с предустановленным Chromium, где
    `playwright install` недоступен. По умолчанию ничего не меняет.
    """
    executable = os.environ.get("CHROMIUM_EXECUTABLE_PATH")
    if executable:
        return {**browser_type_launch_args, "executable_path": executable}
    return browser_type_launch_args

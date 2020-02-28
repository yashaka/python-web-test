import pytest
from selene.support.shared import browser


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    """
    Here, before yield,
    goes all "setup" code for each test case
    aka "before test function" hook
    """
    browser.config.timeout = 2
    # todo: add your before setup here...

    yield

    """
    Here, after yield,
    goes all "tear down" code for each test case
    aka "after test function" hook
    """
    # todo: add your after setup here...
    browser.quit()

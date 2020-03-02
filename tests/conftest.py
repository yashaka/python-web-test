import pytest
import allure
from selene.core.exceptions import TimeoutException
from selene.support.shared import browser


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    """
    Here, before yield,
    goes all "setup" code for each test case
    aka "before test function" hook
    """

    browser.config.timeout = 2

    def attach_snapshots_on_failure(error: TimeoutException) -> Exception:
        last_screenshot = browser.config.last_screenshot
        if last_screenshot:
            allure.attach.file(source=last_screenshot,
                               name='screenshot on failure',
                               attachment_type=allure.attachment_type.PNG)

        last_page_source = browser.config.last_page_source
        if last_page_source:
            allure.attach.file(source=last_page_source,
                               name='page source on failure',
                               attachment_type=allure.attachment_type.HTML)
        return error
    browser.config.hook_wait_failure = attach_snapshots_on_failure

    # todo: add your before setup here...

    # here actual test case will start

    yield

    # here actual test case will stop

    """
    Here, after yield,
    goes all "tear down" code for each test case
    aka "after test function" hook
    """

    # todo: add your after setup here...

    browser.quit()


# todo: fix example... it does not actually work...:(
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def attach_last_screenshot_and_page_source():
#     """
#     These attachments (added from hookimpl fixture)
#     should go into Test Body
#     """
#     prev_test_screenshot = browser.config.last_screenshot
#     prev_test_page_source = browser.config.last_page_source
#
#     yield
#
#     last_screenshot = browser.config.last_screenshot
#     if last_screenshot and not last_screenshot == prev_test_screenshot:
#         allure.attach.file(source=last_screenshot,
#                            name='screenshot on failure',
#                            attachment_type=allure.attachment_type.PNG)
#
#     last_page_source = browser.config.last_page_source
#     if last_page_source and not last_page_source == prev_test_page_source:
#         allure.attach.file(source=last_page_source,
#                            name='page source on failure',
#                            attachment_type=allure.attachment_type.HTML)

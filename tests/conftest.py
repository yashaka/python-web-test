import pytest
import allure
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from selene.support.shared import browser

import project
import web_test.helpers.allure.gherkin


def pytest_addoption(parser):
    project.Config.register(parser)


@pytest.fixture
def config(request):
    if not project.config:
        project.config = project.Config(request)
    return project.config


@pytest.fixture(scope='function', autouse=True)
def browser_management(config):
    """
    Here, before yield,
    goes all "setup" code for each test case
    aka "before test function" hook
    """

    # def attach_snapshots_on_failure(error: TimeoutException) -> Exception:
    #     """
    #     An example of selene hook_wait_failure that attaches snapshots to failed test step.
    #     It is actually not needed and optional,
    #     because in the pytest_runtest_makereport hook below
    #     we attach screenshots to the test body itself,
    #     that is more handy during analysis of test report
    #
    #     but if you need it, you can enable it by uncommenting
    #     together with the following ``browser.config.hook_wait_failure =`` line;)
    #
    #     otherwise, you can remove it
    #     """
    #     last_screenshot = browser.config.last_screenshot
    #     if last_screenshot:
    #         allure.attach.file(source=last_screenshot,
    #                            name='screenshot on failure',
    #                            attachment_type=allure.attachment_type.PNG)
    #
    #     last_page_source = browser.config.last_page_source
    #     if last_page_source:
    #         allure.attach.file(source=last_page_source,
    #                            name='page source on failure',
    #                            attachment_type=allure.attachment_type.HTML)
    #     return error
    # browser.config.hook_wait_failure = attach_snapshots_on_failure

    browser.config.timeout = config.timeout
    browser.config.save_page_source_on_failure \
        = config.save_page_source_on_failure

    # todo: add your before setup here...

    yield

    """
    Here, after yield,
    goes all "tear down" code for each test case
    aka "after test function" hook
    """

    # todo: add your after setup here...

    browser.quit()


prev_test_screenshot = None
prev_test_page_source = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    yield

    global prev_test_screenshot
    prev_test_screenshot = browser.config.last_screenshot
    global prev_test_page_source
    prev_test_page_source = browser.config.last_page_source


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    """
    Attach snapshots on test failure
    """

    # All code prior to yield statement would be ran prior
    # to any other of the same fixtures defined

    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    result = outcome.get_result()

    if web_test.helpers.allure.gherkin.when == 'call' and result.failed:
        last_screenshot = browser.config.last_screenshot
        if last_screenshot and not last_screenshot == prev_test_screenshot:
            allure.attach.file(source=last_screenshot,
                               name='screenshot',
                               attachment_type=allure.attachment_type.PNG)

        last_page_source = browser.config.last_page_source
        if last_page_source and not last_page_source == prev_test_page_source:
            allure.attach.file(source=last_page_source,
                               name='page source',
                               attachment_type=allure.attachment_type.HTML)

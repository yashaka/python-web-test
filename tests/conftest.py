import pytest
import allure
import web_test
from selene.support.shared import browser


@pytest.fixture(scope='session', autouse=True)
def add_reporting_to_selene_steps():

    original_open = browser.open

    from web_test.help.python import monkey
    from selene.support.shared import SharedConfig, SharedBrowser

    @monkey.patch_method_in(SharedBrowser)
    def open(self, relative_or_absolute_url: str):
        from web_test.help.allure import report

        return report.step(original_open)(relative_or_absolute_url)

    @monkey.patch_method_in(SharedConfig)                                       # todo: consider patching Wait explicitly
    def wait(self, entity):
        hook = self._inject_screenshot_and_page_source_pre_hooks(
            self.hook_wait_failure
        )

        from web_test.help.selene.report.wait import ReportedWait
        return ReportedWait(
            entity,
            at_most=self.timeout,
            or_fail_with=hook
        )


import config


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    """
    Here, before yield,
    goes all "setup" code for each test case
    aka "before test function" hook
    """

    import config
    browser.config.base_url = config.settings.base_url
    browser.config.timeout = config.settings.timeout
    browser.config.save_page_source_on_failure \
        = config.settings.save_page_source_on_failure

    browser.config.driver = _driver_from(config.settings)

    yield
    """
    Here, after yield,
    goes all "tear down" code for each test case
    aka "after test function" hook
    """

    browser.config.hold_browser_open = config.settings.hold_browser_open
    if not config.settings.hold_browser_open:
        browser.quit()


from web_test.help.selenium.typing import WebDriver


def _driver_from(settings: config.Settings) -> WebDriver:
    driver_options = _driver_options_from(settings)

    from selenium import webdriver
    driver = web_test.help.webdriver_manager.set_up.local(
        settings.browser_name,
        driver_options,
    ) if not settings.remote_url else webdriver.Remote(
        command_executor=settings.remote_url,
        options=driver_options,
    )

    if settings.maximize_window:
        driver.maximize_window()
    else:
        driver.set_window_size(
            width=settings.window_width,
            height=settings.window_height,
        )

    # other driver configuration todos:
    # file upload when remote
    # - http://allselenium.info/file-upload-using-python-selenium-webdriver/
    #   - https://sqa.stackexchange.com/questions/12851/how-can-i-work-with-file-uploads-during-a-webdriver-test

    return driver


from web_test.help.selenium.typing import WebDriverOptions


def _driver_options_from(settings: config.Settings) -> WebDriverOptions:
    options = None

    from selenium import webdriver
    from web_test.help.webdriver_manager import supported
    if settings.browser_name in [supported.chrome, supported.chromium]:
        options = webdriver.ChromeOptions()
        options.headless = config.settings.headless

    if settings.browser_name == supported.firefox:
        options = webdriver.FirefoxOptions()
        options.headless = config.settings.headless

    if settings.browser_name == supported.ie:
        options = webdriver.IeOptions()

    from web_test.help.selenium.typing import EdgeOptions
    if settings.browser_name == supported.edge:
        options = EdgeOptions()

    from web_test.help.selenium.typing import OperaOptions
    if settings.browser_name == supported.edge:
        options = OperaOptions()

    if settings.remote_url:
        options.set_capability('screenResolution',
                               settings.remote_screenResolution)
        options.set_capability('enableVNC', settings.remote_enableVNC)
        options.set_capability('enableVideo', settings.remote_enableVideo)
        options.set_capability('enableLog', settings.remote_enableLog)
        if settings.remote_version:
            options.set_capability('version', settings.remote_version)
        if settings.remote_platform:
            options.set_capability('platform', settings.remote_platform)

    return options


prev_test_screenshot = None
prev_test_page_source = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    yield

    global prev_test_screenshot
    prev_test_screenshot = browser.config.last_screenshot
    global prev_test_page_source
    prev_test_page_source = browser.config.last_page_source


from _pytest.nodes import Item
from _pytest.runner import CallInfo


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    """
    Attach snapshots on test failure
    """

    # All code prior to yield statement would be ran prior
    # to any other of the same fixtures defined

    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks

    result = outcome.get_result()

    if result.when == 'call' and result.failed:
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

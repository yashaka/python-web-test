import allure
from selene.core.exceptions import TimeoutException
from selene.support.shared import browser


def attach_snapshots_on_failure(error: TimeoutException) -> Exception:
    """
    An example of selene hook_wait_failure that attaches snapshots to failed test step.
    It is actually might not needed,
    because using pytest_runtest_makereport hook
    you can achieve similar
    by attaching screenshots to the test body itself,
    that is more handy during analysis of test report

    but if you need it, you can use it by adding to your browser setup fixture::

        import web_test
        browser.config.hook_wait_failure = \
            web_test.help.selene.shared.hook.attach_snapshots_on_failure

    otherwise, you can skip it;)
    """
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

"""
This module is to integrate allure markers (labels/tags) into pytest markers.
So we can label test cases and achieve two things at once:
- log them correspondingly in allure report
- filter test cases when running via `pytest -m` option

When extending this module with more markers,
ensure you update the pytest.ini file correspondingly;)

Additional Resources:
- https://docs.qameta.io/allure/#_pytest
  - https://docs.qameta.io/allure/#_tags
- https://docs.pytest.org/en/latest/example/markers.html
- https://github.com/pytest-dev/pytest-rerunfailures
"""

import pytest
import allure

from web_test.help.pytest.skip import pending as _pending

pending = _pending
"""
test is pending (to be automated later) and will be skipped during pytest run
"""


class suite:
    @staticmethod
    def smoke(func):
        return pytest.mark.smoke(allure.suite('smoke')(func))


class tag:
    @staticmethod
    def unstable(func):
        return pytest.mark.unstable(allure.tag('unstable')(func))

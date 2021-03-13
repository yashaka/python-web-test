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


def pending(test_fn):                                                           # todo: consider impl as pytest fixture
    def decorated(*args, **kwargs):
        test_fn(*args, **kwargs)
        pytest.skip('as pending')
    return decorated


import functools


@functools.wraps(pytest.mark.flaky)
def flaky(func=..., *, reruns: int = 0, reruns_delay: int = 0, condition=True):
    """
    alias to pytest.mark.flaky(reruns, reruns_delay)
    from pytest-rerunfailures plugin
    (no need to mention in pytest.ini)
    """

    @functools.wraps(pytest.mark.flaky)
    def allurish_decorator(func_):
        return pytest.mark.flaky(
            reruns=reruns,
            reruns_delay=reruns_delay,
            condition=condition,
        )(allure.tag('flaky')(func_))

    return allurish_decorator(func) if callable(func) else allurish_decorator


class suite:
    @staticmethod
    @functools.wraps(pytest.mark.smoke)
    def smoke(func):
        return pytest.mark.smoke(allure.suite('smoke')(func))


class tag:
    @staticmethod
    @functools.wraps(pytest.mark.in_progress)
    def in_progress(func):
        return pytest.mark.in_progress(allure.tag('in_progress')(func))

    @staticmethod
    @functools.wraps(pytest.mark.fast)
    def fast(func):
        return pytest.mark.fast(allure.tag('fast')(func))

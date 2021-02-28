import pytest


def pending(test_fn):                                                           # todo: consider impl as pytest fixture
    def decorated(*args, **kwargs):
        test_fn(*args, **kwargs)
        pytest.skip('as pending')
    return decorated

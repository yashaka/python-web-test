import logging
from functools import reduce
from typing import Tuple, List
import allure_commons
from allure_commons._core import MetaPluginManager
from allure_commons.utils import uuid4


def log_with(
    *,
    translations: List[Tuple[str, str]] = (),
):
    """
    returns decorator factory with logging to specified logger
    with added list of translations
    to decorate Selene's waiting via config._wait_decorator
    """

    def decorator_factory(wait):
        def decorator(for_):
            def decorated(fn):

                title = f'{wait.entity}: {fn}'

                def translate(initial: str, item: Tuple[str, str]):
                    old, new = item
                    return initial.replace(old, new)

                translated_title = reduce(
                    translate,
                    translations,
                    title,
                )

                with _StepContext(title=translated_title):
                    return for_(fn)

            return decorated

        return decorator

    return decorator_factory


class _StepContext:
    def __init__(
        self,
        title,
        params=None,
        plugin_manager: MetaPluginManager = allure_commons.plugin_manager,
    ):
        self.title = title
        self.params = params or {}
        self.uuid = uuid4()
        self.plugin_manager = plugin_manager

    def __enter__(self):
        self.plugin_manager.hook.start_step(
            uuid=self.uuid,
            title=self.title,
            params=self.params,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.plugin_manager.hook.stop_step(
            uuid=self.uuid,
            title=self.title,
            exc_type=exc_type,
            exc_val=exc_val,
            exc_tb=exc_tb,
        )

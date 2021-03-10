from typing import Callable

from selene.core.wait import Wait as SeleneWait, E, R

from web_test.helpers.allure.report import step


class ReportedWait(SeleneWait[E]):

    def for_(self, fn: Callable[[E], R]) -> R:
        original = super().for_

        @step(
            display_context=False,
            params_separator=': ',
            derepresent_params=True,
            translations=(
                    ('browser.element', 'element'),
                    ('browser.all', 'all'),
                    ("'css selector', ", ""),
                    (r"'\ue007'", "Enter"),
                    ('((', '('),
                    ('))', ')'),
                    (': has ', ': have '),
                    (': have ', ': should have '),
                    (': is ', ': should be'),
            )
        )
        def _(locator, action) -> R:
            return original(fn)

        return _(str(self._entity), str(fn))

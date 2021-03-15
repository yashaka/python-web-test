from typing import Callable

from selene.core.wait import Wait as SeleneWait, E, R


class ReportedWait(SeleneWait[E]):

    def for_(self, fn: Callable[[E], R]) -> R:
        original = super().for_

        from web_test import help

        @help.allure.report.step(
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

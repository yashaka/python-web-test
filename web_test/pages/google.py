from __future__ import annotations

from web_test.helpers.allure.report import step

"""
The previous line is needed to type hint classes that are defined later
like Results class below
"""


from selene import by, have
from selene.support.shared import browser


class Google:
    """
    This is a simpler example of PageObject pattern appliance.
    Here we use one pageobject instead of two

    Also, here we extensively use "fluent" style of "PageObject",
    aka Fluent PageObject pattern, when each method return an object
    of kind of "next page"... But this "next page" nuance is tricky...
    Read more in follow_result_link docstrings;)
    """
    def __init__(self):
        self.results = browser.all('#search .g')

    @step
    def open(self) -> Google:
        browser.open('https://google.com/ncr')
        return self

    @step
    def search(self, text) -> Google:
        browser.element(by.name('q')).type(text).press_enter()
        return self

    @step
    def should_have_result(self, index, text) -> Google:
        self.results[index].should(have.text(text))
        return self

    @step
    def should_have_results_amount_at_least(self, number) -> Google:
        self.results.should(have.size_greater_than_or_equal(number))
        return self

    @step
    def follow_result_link(self, text):
        """
        Here we could return "next page object",
        following so called Fluent PageObject pattern
        but usually it might lead to confusion in such cases.
        For example, what if we fail to follow the link
        and this is "as expected", e.g. according to our
        "negative" test case conditions.
        Then it's logically to expect "same pageobject" not "next one"
        Now we have two potential state as a result of this method execution.
        And it's not clear what to return;)
        So better to return "void"/None in such cases.
        Usually Fluent PageObject makes sense only in cases
        with only 1 possible result state, for example:
        - returning self (we for sure stay on the same page)
        - returning "sub-page-object" i.e. object of component on the page
          (it's always there)
        """
        self.results.element_by(have.text(text)).element('a').click()


google: Google = Google()
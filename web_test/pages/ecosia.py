from __future__ import annotations

from web_test.helpers.allure.report import step

"""
The previous line is needed to type hint classes that are defined later
like Results class below
"""


from selene import by, have
from selene.support.shared import browser


class Ecosia:

    @step
    def open(self):
        browser.open('https://www.ecosia.org/')

    @step
    def search(self, text):
        browser.element(by.name('q')).type(text).press_enter()

    @property
    def results(self) -> Results:
        return Results()


class Results:

    def __init__(self):
        self.elements = browser.all('.result')

    @step
    def should_have_size_at_least(self, amount) -> Results:
        self.elements.should(have.size_greater_than_or_equal(amount))
        return self

    @step
    def should_have_text(self, index, value) -> Results:
        self.elements[index].should(have.text(value))
        return self

    @step
    def follow_link(self, index):
        self.elements[index].element('a').click()


ecosia: Ecosia = Ecosia()

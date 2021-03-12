from selene import have
from selene.support.shared import browser
from web_test.help.allure.report import step

"""
The file is named with _org in the end just to make it more explicit –
that this official python site page
"""

_url = 'https://www.python.org/'

_results = browser.all('.list-recent-events>li')


@step
def open():
    browser.open(_url)


@step
def should_be_opened():
    browser.should(have.url(_url))


@step
def search(text):
    browser.element('#id-search-field').type(text).press_enter()


@step
def should_have_result(index, text):
    _results[index].should(have.text(text))

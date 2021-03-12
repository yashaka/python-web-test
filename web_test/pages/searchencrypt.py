from selene import by, have
from selene.support.shared import browser

from web_test.help.allure.report import step

"""
This is a simplest possible implementation of pages model. 
It is based on simple features of "Modular Paradigm" (over OOP).
It's dead simple, aka KISS, which has a lot of benefits, like
ability to quickly train a junior team in extending automation coverage.

Though it lacks some "oop style" features, like "chainable fluent" style.  
I.e. instead of

    web.google\
        .search('selene python')\
        .should_have_results_amount_at_least(5)
        
you have to write:

    web.google.search('selene python')\
    web.google.should_have_results_amount_at_least(5)

Technically it's possible to make the "fluent" style work, by something like this:

    import sys
    self = sys.modules[__name__]
    
    def search(text):
        # impl...
        return self

But... The autocomplete will not work in such case... 
Hence, better not to over-complicate;)
"""


results = browser.all('.web-result')


@step
def visit():
    """
    Also, here... we have to rename open to visit,
    in order to eliminate potential conflicts
    with python built in `open` function
    """
    browser.open('https://www.searchencrypt.com')


@step
def search(text):
    browser.element(by.name('q')).type(text)
    submit = browser.element('.fas.fa-search')
    submit.click()


@step
def should_have_result(index, text):
    results[index].should(have.text(text))


@step
def should_have_results_amount_at_least(number):
    results.should(have.size_greater_than_or_equal(number))


@step
def follow_result_link(text):
    results.element_by(have.text(text)).element('a').click()
    browser.switch_to_next_tab()

# This file contains examples of different "modeling styles" when implementing tests.
# The algorithm of choosing your way to write tests might be the following:
# 1. Start reviewing examples from top to bottom
# 2. Stop where you understand what happens yet AND you like it
#    But ensure you quickly check at least a few more examples;) Just in case;)
#    Ensure you check the Allure Report for corresponding example.
# 3. Remove all not needed examples
#    and corresponding python modules that are used in them
# 4. Stick to the style chosen;)
#
# Of course you can mix styles, if you understand what you do;)
#
# Ensure you check the Allure Report of corresponding test examples.
# * The test style will influence the reporting too
# * what is good to count when making your choice

import pytest


def test_bing():
    """
    Pending test example (Option 1)
    ===============================

    opened bing.com
    search 'yashaka selene python'
    results should be of count more than 5, first text '... Web UI ...'
    follows first link
    should be on github repo 'yashaka/selene'
    """
    pytest.skip('as pending')


from web_test.test_markers import mark


@mark.pending                                                                        # todo: find a way to automatically skip empty tests, maybe use some pytest plugin
def test_yahoo():
    """
    Pending test example (Option 2)
    ===============================

    opened yahoo.com
    search 'yashaka selene python'
    results should be of count more than 5, first text '... Web UI ...'
    follows first link
    should be on github repo 'yashaka/selene'
    """


from selene.support.shared import browser
from selene import have, be
"""
... the only 3 things you need to import 
    to start working with Selene in a straightforward KISS style;)
"""


@mark.suite.smoke
def test_duckduckgo():
    """
    Straightforward/PageObjectLess style
    ===================================

    GO FOR:
    * KISS (Keep It Simple Stupid), straightforward style
      * easy for newbies in automation (no need to learn modules/OOP(classes))
      * easy for some DEVs if they will use these tests (and they should!)
        they know selectors and internals of app they develop
        hence, building more abstractions (modules/classes) on top of more
        low level straightforward code (like below) would add too much complexity
        to them, and harder in day-to-day usage

    TRADEOFFS:
    - given selectors are duplicated all over the project code base
      when you want to change it
      then you have to use global Find&Replace text,
           with sometimes pretty thorough manual checks line by line
           all places where the change will be applied.
           You CAN'T use some refactoring features of IDE like Refactor>Rename
    """

    browser.open('https://duckduckgo.com/')

    browser.element('[name=q]')\
        .should(be.blank)\
        .type('yashaka selene python').press_enter()
    browser.all('.result__body') \
        .should(have.size_greater_than(5)) \
        .first.should(have.text('User-oriented Web UI browser tests'))

    browser.all('.result__body').first.element('a').click()
    browser.should(have.title_containing('yashaka/selene'))


from selene.support.shared.jquery_style import s, ss
"""
some JQuery style shortcuts, if considered sexy, can help with conciseness;)
"""


def test_duckduckgo_():
    """
    Straightforward/PageObjectLess style + s, ss for JQuery/Selenide's $, $$
    ========================================================================

    GO FOR:
    * the most concise
    * KISS (Keep It Simple Stupid), straightforward style
      * easy for newbies in automation (no need to learn modules/OOP(classes))
      * easy for some DEVs if they will use these tests (and they should!)
        they know selectors and internals of app they develop
        hence, building more abstractions (modules/classes) on top of more
        low level straightforward code (like below) would add too much complexity
        to them, and harder in day-to-day usage

    TRADEOFFS:
    - given selectors are duplicated all over the project code base
      when you want to change it
      then you have to use global Find&Replace text,
           with sometimes pretty thorough manual checks line by line
           all places where the change will be applied.
           You CAN'T use some refactoring features of IDE like Refactor>Rename
    """
    browser.open('https://duckduckgo.com/')

    s('[name=q]').type('yashaka selene python').press_enter()
    ss('.result__body') \
        .should(have.size_greater_than(5)) \
        .first.should(have.text('User-oriented Web UI browser tests'))

    ss('.result__body').first.s('a').click()
    browser.should(have.title_containing('yashaka/selene'))


from web_test.pages import pypi
"""
# where pypi is your locators storage –
# as simple as simple python module 
# (listed here for easier demo)

from selene.support.shared import browser

url = 'https://pypi.org/'

search = browser.element('#search')
results = browser.all('.package-snippet')
"""


def test_pypi():
    """
    LocatorModules/PageObjectLess
    LocatorModules == page locators/selectors are simply vars in python modules
    Might be also called as PageModules
    ===========================================================================

    Here the page model is implemented in the simplest modular way
    with simplification to "just vars, no functions for steps" in python modules.

    GO FOR:
    * a bit higher abstraction (no more technical selectors in tests code)
      * extra readability in test code
    * reusable vars with locators
    * easier refactoring (Refactor>Rename, etc. can be applied)
    * yet KISS modeling (Keep It Simple Stupid)

    TRADEOFFS:
    - common ones for "programming without functions" style ;)
      some code might be too bulky,
      business steps might be hardly visible in a long e2e test
   """
    browser.open(pypi.url)

    pypi.search.type('selene').press_enter()
    pypi.results\
        .should(have.size_greater_than_or_equal(9)) \
        .first.should(have.text('Concise API for selenium in Python'))

    pypi.results.first.click()
    browser.should(have.url(pypi.url + 'project/selene/'))
    browser.should(have.title_containing('selene · PyPI'))


from web_test.help.allure.gherkin import when, given, then
"""
for extra BDD-style decoration with extra comments to log in report
"""


def test_duckduckgo__():
    """
    Straightforward/PageObjectLess/BDD style + reported "steps-comments" (Option 1)
    ==============================================================================

    GO FOR:
    * KISS (Keep It Simple Stupid), straightforward style
    * extra readability and structure in both Test and its Report
      * to add comments reflecting some test logic from higher business perspective
      * to break the long End-to-End test into meaningful chunks
        (the code below in not actually so long, but just for example;))

    TRADEOFFS:
    - extra "texts" to support in code
    - steps can't be reused                                                     # todo: there are some ideas though;)
    - too much of test-like-steps might made code less focused, too vague
      especially when repeating the logic or test data as it is already used in code
    - Manual old-fashioned Find&Replace instead of Refactor>Rename

    NOTES
    * you can use 3 AAA naming over BDD:
      @arrange over @given
      @act over @then
      @assert_ over @then

    * you can call step fn whatever you like, examples:

        @when('search')
        def step(text='selene python'):
            browser.element('[name=q]').type(text).press_enter()

        @when()
        def search(text='selene python'):
            browser.element('[name=q]').type(text).press_enter()

        @when('search')
        def params(text='selene python'):
            browser.element('[name=q]').type(text).press_enter()

        @when('search')
        def args(text='selene python'):
            browser.element('[name=q]').type(text).press_enter()

        @when('search')
        def ine(text='selene python'):
            browser.element('[name=q]').type(text).press_enter()

        @when('search')
        def _(text='selene python'):
            browser.element('[name=q]').type(text).press_enter()

        ;)

    * you can skip params at all,
      if you don't need them to be logged in report
      as high level step's test data

        @when('search')
        def ine():
            browser.element('[name=q]').type('selene python').press_enter()

        @when()
        def search():
            browser.element('[name=q]').type('selene python').press_enter()

    * take into account that this is mostly a bad practice –
      to DUPLICATE test data in "step comments" –
      you bloat code with same info and increase support time on each change

        @when('search "selene python"')
        def ine():
            browser.element('[name=q]').type('selene python').press_enter()
    """

    @given('opened duckduckgo')
    def step():
        browser.open('https://duckduckgo.com/')

    @when('search')
    def step(text='yashaka selene python'):
        s('[name=q]').type(text).press_enter()

    @then('results should be')
    def step(more_than=5,
             first_result_text='User-oriented Web UI browser tests'):
        ss('.result__body') \
            .should(have.size_greater_than(more_than)) \
            .first.should(have.text(first_result_text))

    @when('follows first link')
    def step():
        ss('.result__body').first.element('a').click()

    @then('should be on github')
    def step(repo='yashaka/selene'):
        browser.should(have.title_containing(repo))


def test_duckduckgo___():
    """
    Straightforward/PageObjectLess/BDD style + reported "steps-comments" (Option 2)
    ==============================================================================

    GO FOR:
    * KISS (Keep It Simple Stupid), straightforward style
    * extra readability and structure in both Test and its Report
      ... see more in previous example

    TRADEOFFS:
    - extra "texts" to support in code
    - steps can't be reused
    - Manual old-fashioned Find&Replace instead of Refactor>Rename
    """

    @given()
    def opened_duckduckgo():
        browser.open('https://duckduckgo.com/')

    @when()
    def search(text='yashaka selene python'):
        browser.element('[name=q]').type(text).press_enter()

    @then()
    def results_should_be(
        more_than=5,
        first_result_text='User-oriented Web UI browser tests'
    ):
        browser.all('.result__body')\
            .should(have.size_greater_than(more_than))\
            .first.should(have.text(first_result_text))

    @when()
    def follows_first_link():
        browser.all('.result__body').first.element('a').click()

    @then()
    def should_be_on_github(repo='yashaka/selene'):
        browser.should(have.title_containing(repo))


from web_test.pages import searchencrypt, python_org
"""
abstracting things out into more high level step-functions in simple python modules
"""


@mark.suite.smoke
@mark.flaky(reruns=1)
def test_searchencrypt():
    """
    PageModules/PageObjectLess
    PageModules == page steps are simply functions in python modules
    ================================================================

    Here the page model is implemented in the simplest modular way.
    The `searchencrypt` is page module (python module with functions)
    not page object (a python object of class with methods)

    GO FOR:
    * higher abstraction (no lower tech details in tests code)
      * extra readability in both Test and its Report
    * reusable steps
    * easier refactoring (Refactor>Rename, etc. can be applied)
    * yet KISS modeling (Keep It Simple Stupid)

    TRADEOFFS:
    - extra bloated functions sometimes repeating already readable raw/straightforward selene code
    - common tradeoffs for Modular/Procedural paradigm in Python
      - potentially less readable in complex modeling scenarios
        - functions can become complicated when have many parameters
        - procedural composition looks less sexy as object oriented in python
          - TODO: provide example
        - no fluent style like page.results.first.follow_link()
    """
    searchencrypt.visit()

    searchencrypt.search('python')
    searchencrypt.should_have_results_amount_at_least(5)

    searchencrypt.follow_result_link('Welcome to Python.org')
    python_org.should_be_opened()


# === Notes ===
# Take into account that here we don't differentiate between
# * Page(Object/etc.)
# and
# * Steps(Object/etc.)
# Usually such separation is relevant only in extremely complicated applications
# which are pretty rare in real life. In the majority of situations, to simplify
# the application model implementation, it's easier to decompose "*Objects"
# into smaller ones at the same layer of abstraction, not adding one more layer.
# Since tests nevertheless should test "user behavioural steps",
# it's natural to start refactoring the straightforward code to user-steps-functions
# This allows us to forget about advantages of "assertion-free PageObjects" approach.
# Since it's natural to consider "assertion methods" also "user steps" and
# put them at same place ;)
# Many things becomes easier then;)
# =================================


from web_test import app
"""
collecting everything into one place for easier and faster access
"""


@mark.tag.in_progress
@mark.flaky
def test_searchencrypt_():
    """
    PageModules/PageObjectLess + ApplicationManager
    ===============================================

    GO FOR:
    * one entry point to all app model, you import it once as app and
      gain access to all available pages without trying to remember them
    * ... see more at test_searchencrypt example

    TRADEOFFS:
    - supporting all page imports in a separate file
    - ... same as for test_searchencrypt example
    """
    app.searchencrypt.visit()

    app.searchencrypt.search('python')
    app.searchencrypt.should_have_results_amount_at_least(5)

    app.searchencrypt.follow_result_link('Welcome to Python.org')
    app.python_org.should_be_opened()


from web_test.pages.google import Google
google = Google()


def test_google():
    """
    Here we use simplified implementation
    with one page object (google)
    It's implemented in "fluent style",
    where its methods return self,
    where possible.

    Notice, that technically we could write everything
    in "one chain"

    web.google\
        .open()\
        .search('selene python')\
        .should_have_results_amount_at_least(5)\
        .search('selene python')\
        .should_have_results_amount_at_least(5)
        .follow_result_link('User-oriented Web UI browser tests')

    web.github.should_be_on('yashaka/selene')

    But such a code lacks "structure".
    It's hardly visible from one sight
    how much steps does this scenario have

    Take this into account.
    Fluent style is handy, but not overuse it;)

    """
    google.open()

    google \
        .search('yashaka selene python') \
        .should_have_results_amount_at_least(12)  # demo-failure ;)
    #   .should_have_results_amount_at_least(5)

    google.follow_result_link('User-oriented Web UI browser tests')
    github.should_be_on('yashaka/selene')


from web_test.pages.ecosia import ecosia
from web_test.pages.github import github


def test_ecosia():
    ecosia.open()

    ecosia.search(text='yashaka selene python')
    ecosia.results \
        .should_have_size_at_least(5) \
        .should_have_text(0, 'User-oriented Web UI browser tests')

    ecosia.results.follow_link(0)
    github.should_be_on('yashaka/selene')


def test_ecosia_():
    app.ecosia.open()

    app.ecosia.search(text='yashaka selene python')
    app.ecosia.results \
        .should_have_size_at_least(5) \
        .should_have_text(0, 'User-oriented Web UI browser tests')

    app.ecosia.results.follow_link(0)
    app.github.should_be_on('yashaka/selene')

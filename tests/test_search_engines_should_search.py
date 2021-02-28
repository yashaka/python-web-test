import pytest
from selene import have
from selene.support.shared import browser
from selene.support.shared.jquery_style import s, ss

from web_test import app
from web_test.helpers.allure.gherkin import when, given, then
from web_test.helpers.pytest.skip import pending


def test_bing():
    """
    Pending test example (Option 2)
    ===============================

    opened bing.com
    search 'yashaka selene python'
    results should be of count more than 5, first text '... Web UI ...'
    follows first link
    should be on github repo 'yashaka/selene'
    """
    pytest.skip('as pending')


@pending                                                                        # todo: find a way to automatically skip empty tests
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

    browser.element('[name=q]').type('yashaka selene python').press_enter()
    browser.all('.result__body') \
        .should(have.size_greater_than(5)) \
        .first.should(have.text('User-oriented Web UI browser tests'))

    browser.all('.result__body').first.element('a').click()
    browser.should(have.title_containing('yashaka/selene'))


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

    ss('.result__body').first.element('a').click()
    browser.should(have.title_containing('yashaka/selene'))


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

        @when()
        def search():
            browser.element('[name=q]').type('selene python').press_enter()

        @when('search')
        def ine():
            browser.element('[name=q]').type('selene python').press_enter()

    """

    @given('opened duckduckgo')
    def step():
        browser.open('https://duckduckgo.com/')

    @when('search')
    def step(text='yashaka selene python'):
        browser.element('[name=q]').type(text).press_enter()

    @then('results should be')
    def step(more_than=5,
             first_result_text='User-oriented Web UI browser tests'):
        browser.all('.result__body')\
            .should(have.size_greater_than(more_than))\
            .first.should(have.text(first_result_text))

    @when('follows first link')
    def step():
        browser.all('.result__body').first.element('a').click()

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


def test_duckduckgo____():
    """
    Below we access pageobjects (duckduckgo, github)
    through a so called "root entry point" (implemented as python module)
    aka "application manager" or "pages manager".
    You also can access pageobjects directly, like in test_ecosia() test
    Read more on this in app.py module docstrings
    """
    app.duckduckgo.open()

    app.duckduckgo.search('yashaka selene python')
    app.duckduckgo.results \
        .should_have_size_at_least(5) \
        .should_have_text(0, 'User-oriented Web UI browser tests')

    app.duckduckgo.results.follow_link(0)
    app.github.should_be_on('yashaka/selene')


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
    app.google.open()

    app.google \
        .search('yashaka selene python') \
        .should_have_results_amount_at_least(12)  # demo-failure ;)
    #   .should_have_results_amount_at_least(5)

    app.google.follow_result_link('User-oriented Web UI browser tests')
    app.github.should_be_on('yashaka/selene')


def test_searchencrypt():
    """
    Here the page model is implemented in the simplest modular way.
    Here searchencrypt is page module (python module with functions)
    not page object (a python object of class with methods)

    Here we can't use "fluent style" in full power
    But the implementation is dead simple, aka KISS
    That has a lot of benefits, especially for the team
    full of junior and manual engineers involved
    """
    app.searchencrypt.visit()

    app.searchencrypt.search('github.com')
    app.searchencrypt.should_have_results_amount_at_least(5)

    app.searchencrypt.follow_result_link('Where the world builds software')
    app.github.should_be_on('GitHub')

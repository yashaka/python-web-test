from web_test import web


def test_duckduckgo():
    """
    Below we access pageobjects (duckduckgo, github)
    through a so called "root entry point" (implemented as python module)
    aka "application manager" or "pages manager".
    You also can access pageobjects directcly, like in test_ecosia() test
    Read more on this in web.py module docstrings
    """
    web.duckduckgo.open()

    web.duckduckgo.search('selene python')
    web.duckduckgo.results \
        .should_have_size_at_least(5) \
        .should_have_text(0, 'User-oriented Web UI browser tests')

    web.duckduckgo.results.follow_link(0)
    web.github.should_be_on('yashaka/selene')


from web_test.pages.ecosia import ecosia
from web_test.pages.github import github


def test_ecosia():
    ecosia.open()

    ecosia.search('selene python')
    ecosia.results\
        .should_have_size_at_least(5)\
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
    web.google.open()

    web.google\
        .search('selene python')\
        .should_have_results_amount_at_least(12)
        # .should_have_results_amount_at_least(5)

    web.google.follow_result_link('User-oriented Web UI browser tests')
    web.github.should_be_on('yashaka/selene')


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
    web.searchencrypt.visit()

    web.searchencrypt.search('selene python')
    web.searchencrypt.should_have_results_amount_at_least(5)

    web.searchencrypt.follow_result_link('User-oriented Web UI browser tests')
    web.github.should_be_on('yashaka/selene')

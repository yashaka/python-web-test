from web_test.helpers.allure import gherkin


def arrange(description: str):
    return gherkin.given(description)


def act(description: str):
    return gherkin.when(description)


def assert_(description: str):
    return gherkin.then(description)

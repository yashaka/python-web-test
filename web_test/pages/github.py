from selene import have
from selene.support.shared import browser

from web_test.helpers.allure.report import step


class Github:
    @step
    def should_be_on(self, title_text):
        browser.should(have.title_containing(title_text))


github: Github = Github()

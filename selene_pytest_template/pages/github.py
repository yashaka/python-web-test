from selene import have
from selene.support.shared import browser


class Github:
    def should_be_on(self, title_text):
        browser.should(have.title_containing(title_text))


github: Github = Github()

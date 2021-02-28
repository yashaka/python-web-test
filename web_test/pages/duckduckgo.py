from __future__ import annotations

from web_test.helpers.allure.report import step

"""
The previous line is needed to type hint classes that are defined later
like Results class below
"""


from selene import by, have
from selene.support.shared import browser

"""
Instead of "class with methods + object" below
You can simply use raw functions inside the python module.
Hence, you represent pages with modules over objects. 
The implementation will be more simple, aka KISS
But you might miss some features of OOP, object properties, etc...
that you might need with the time

And also, you might miss the general fluent oop style, 
allowing you to write something like: 

    page.table.row(1).cell(2).input.set_value('foo')
    
For example, below we use this when `duckduckgo.results` property 
returns Results object of another "page", 
allowing "fluent chainable style".

But maybe you don't need all these "additions", 
or you can use OOP-style pageobjects 
only for reusable generic widgets,
like: dropdowns, datapickers, tables, etc.

Also take into account your audience:
- if a lot of manual or junior test engineers will write tests
  - then the lesser features you use the better
    - then probably sticking to one style everywhere is better
- if you know what you do, and your audience is mature
  - then probably it's good to start from simplest solution
    - and use advanced features case by case
      when you really need them
"""


class Duckduckgo:
    @step
    def open(self):
        browser.open('https://duckduckgo.com/')

    @step
    def search(self, text):
        browser.element(by.name('q')).type(text).press_enter()

    @property
    def results(self) -> Results:
        return Results()


class Results:

    def __init__(self):
        self.elements = browser.all('.result__body')

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


"""
This object here is needed for faster access to the page object.
Hence you don't need to import class and create and object for it
you can import object directly.

Probably if use use app.py module collecting all such objects in one place
that surves and root entry point to your application model
then you don't need this object defined here. Then you can simple remove it.
"""
duckduckgo: Duckduckgo = Duckduckgo()
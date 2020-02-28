Selene + Pytest tests project template
======================================

Intro
-----

This is a template project. Download it, rename the project folder to something like `my-product-test`, then rename the modules correspondingly (like `selene_pytest_template` to `my_product_test`, etc...), edit the "project" section in `pyproject.toml`::

    [tool.poetry]
    name = "my-product-test"
    version = "0.1.0"
    description = ""
    authors = ["Your Name <your.name@yourcompanymailbox.com>"]

And you should be ready to go ;)

You can also consider keeping the template examples for some time. Maybe just leave `selene_pytest_template` package as it is, and add your own `my_product_test`. Then duplicate the tests folder, edit the copy as you need, while keeping the original `tests` folder under another name, e.g. `examples`;)

Pay attention to a lot of comments and docstrings in code to understand what happens. You will find different styles of implementing page-objects. Probably you will need only one style in your case. So read all explanations and choose the one that fits your needs.

If you are a total beginner and like "simplest" way, consider using the style used in `test_searchencrypt()`. If you are a beginner but want your project to "shine" and avoid "weird questions" from some senior engineers, use the style used in "test_google()` (other styles can be added afterwards).


Installation
------------

Given installed:

* `pyenv + python <https://github.com/pyenv/pyenv>`_
* `poetry <https://poetry.eustace.io/docs/#installation>`_

Do::

    cd $YOUR_PROJECT_FOLDER_PATH
    poetry install


So you can run your tests via::

    poetry run pytest tests/

Or with xdist parallelisation::

    poetry run pytest -n 4 tests/


Details
-------
tbd

TODO list
---------

This template is yet in progress. **Todos** are:

- add support for parsing command line args
- read options from enf files
- more default options examples, like headless mode for browser
- allure reporting integrated
- test suites via pytest marks/tags
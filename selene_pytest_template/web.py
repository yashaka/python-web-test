from selene_pytest_template.pages.duckduckgo import Duckduckgo
from selene_pytest_template.pages.ecosia import Ecosia
from selene_pytest_template.pages.github import Github
from selene_pytest_template.pages.google import Google

"""
This module is optional. 
Usually it makes sense to call it `app.py`,
but in the context of this template project, our app is "all web", 
and the word "web" is already a good name describing exactly what we want.
The idea is to provide a one entry point to all PageObjects
So you can import just this entry point in your test:

    from selene_pytest_template.pages import web
    
and then fluently access any page:

    web.ecosia
    # ...
    web.searchencrypt
    # ...
    web.duckduckgo
    
instead of direct import:

    from selene_pytest_template.pages.ecosia import ecosia
    from selene_pytest_template.pages.searchencrypt import searchencrypt
    from selene_pytest_template.pages.duckduckgo import duckduckgo

    ecosia
    # ...
    searchencrypt
    # ...
    duckduckgo
    
Probably instead of:

    selene_pytest_template/web.py
    
you can use any of:

    selene_pytest_template/pages/web.py
    selene_pytest_template/pages/__init__.py

we type hint variables below to allow better IDE support,
e.g. for Quick Fix feature...
"""
duckduckgo: Duckduckgo = Duckduckgo()
ecosia: Ecosia = Ecosia()
google: Google = Google()


"""
searchencrypt is "PageModule" not "PageObject"
that's we don't have to introduce a new variable for page's object
just an import is enough

There is one nuance though...
If we want the IDE in case of "quick fixing imports" to 
show for us ability to directly import searchencrypt from web.py
then we have to do something like this:

    from selene_pytest_template.pages import searchencrypt as _searchencrypt
    searchencrypt = _searchencrypt
    
But probably you will never need it;)
Hence keep things simple;)
"""
from selene_pytest_template.pages import searchencrypt

github: Github = Github()

from web_test.pages.duckduckgo import Duckduckgo
from web_test.pages.ecosia import Ecosia
from web_test.pages.github import Github
from web_test.pages.google import Google

"""
This module is optional. 
Usually it makes sense to call it `app.py`,
but in the context of this template project, our app is "all web", 
and the word "web" is already a good name describing exactly what we want.
The idea is to provide a one entry point to all PageObjects
So you can import just this entry point in your test:

    from web_test.pages import web
    
and then fluently access any page:

    web.ecosia
    # ...
    web.searchencrypt
    # ...
    web.duckduckgo
    
instead of direct import:

    from web_test.pages.ecosia import ecosia
    from web_test.pages.searchencrypt import searchencrypt
    from web_test.pages.duckduckgo import duckduckgo

    ecosia
    # ...
    searchencrypt
    # ...
    duckduckgo
    
Probably instead of:

    web_test/web.py
    
you can use any of:

    web_test/pages/web.py
    web_test/pages/__init__.py

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

    from web_test.pages import searchencrypt as _searchencrypt
    searchencrypt = _searchencrypt
    
But probably you will never need it;)
Hence keep things simple;)
"""
from web_test.pages import searchencrypt

github: Github = Github()

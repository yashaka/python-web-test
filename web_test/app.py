from web_test.pages.ecosia import Ecosia
from web_test.pages.github import Github
from web_test.pages.google import Google

"""
This module is optional.
It is needed to implement an ApplicationManager pattern
Usually it makes sense to call it `app.py`,
but in the context of this template project, our app is "all web"... 
Hence we could call it simply `web.py`. 
If `pages` name is also good to our taste, 
we could move all this content simply into web_test.pages.__init__.py
Find your style on your own;)

So, the idea is to provide a one entry point to all your model entities, 
that you might implement following some kind of PageObject pattern variations
(PageModule/StepsModule/PageObject/StepsObject/etc)

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

    web_test/app.py
    
you can use any of:

    web_test/pages/app.py
    web_test/pages/__init__.py

we type hint variables below to allow better IDE support,
e.g. for Quick Fix feature...
"""
ecosia: Ecosia = Ecosia()
google: Google = Google()
github: Github = Github()
"""
we need type hints above 
-  to make Autocomplete and Quick Fix features work 
  - at least in some versions of PyCharm
"""

from web_test.pages import searchencrypt
from web_test.pages import python_org
"""
searchencrypt is kind of "PageModule" not "PageObject"
that's why we don't have to introduce a new variable for page's object
just an import is enough

There is one nuance though...
If we want the IDE in case of "quick fixing imports" to 
show for us ability to directly import searchencrypt from app.py
then we might have to do something like this in some versions of your IDEs:

    from web_test.pages import searchencrypt as _searchencrypt
    searchencrypt = _searchencrypt

But probably you will never need it;)
Hence keep things simple;)
"""

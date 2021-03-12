# MIT License
#
# Copyright (c) 2015-2021 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from typing import Literal, Optional

EnvContext = Literal['local', 'prod']
"""
Extend it in accordance with your conditions.

It defines valid env contexts for better IDE support when dealing with them.
- but your Editor of Choice should support it;) 
  - e.g. PyCharm support only from versions >= 2019.3
"""


import pydantic


class Settings(pydantic.BaseSettings):
    """
    Implemented based on pydantic modeling, see:
    - https://pydantic-docs.helpmanual.io/usage/settings/ for docs
    - https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
      for some further conf management ideas

    Some recommendations:
    - add type hints, even if the type can be inferred from the default value
      to store field ordering (just in case... see more on this in docs)

    Things that could be here:
    ==========================
    parallelize: bool = True
    parallelize_in_exact_subprocess_number: Optional[int] = None
    '''
    though it would be consistent and pretty readable to have all potential
    project options at one place,
    the more KISS way is just to keep things as they are in pytest
    and use -n <int> OR -n auto when parallelization is needed

    In future we can play with this and implement it though external plugin
    (yet stored locally in this project)
    '''

    """

    context: EnvContext = 'local'
    """
    controls the environment context, 
    will result in where to load other settings from
    
    'local' is the default value and a special one...
    - the corresponding config.local.env file is ignored in .gitignore
    - so if absent (e.g. on first git clone)
      - the default values defined below will be used
    - if present (e.g. once copied&edited from config.local.env.example)
      - then will be used only locally by you, 
        not mixing stuff for other team members ;)
    """

    timeout: float = 6.0
    hold_browser_open: bool = False
    save_page_source_on_failure: bool = True
    author: str = 'yashaka'
    # base_url: str = 'http://'

    @classmethod
    def in_context(cls, env: EnvContext = None):
        """
        factory method to init Settings with values from corresponding .env file
        """
        asked_or_current = env or cls().context
        return cls(_env_file=f'config.{asked_or_current}.env')


settings = Settings.in_context()
"""
USAGE
=====
import config
browser.config.timeout = config.settings.timeout

===================================
Alternative implementation
- to separate 
  original timeout on process start
  from current timeout
- just in case;)
===================================
# config.py
on_start = Settings.in_context()


def get():
    return Settings.in_context() 

# conftest.py
import config
# ...
browser.config.timeout = config.on_start.timeout
# ...
browser.config.timeout = config.get().timeout
# – or same: –
# browser.config.timeout = config.Settings.in_context().timeout

"""


if __name__ == '__main__':
    """
    for debugging purposes
    to check the actual config values on start
    when simply running `python config.py`
    """
    print(settings.__repr__())

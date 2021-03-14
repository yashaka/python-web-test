from typing import Literal, Optional

EnvContext = Literal['local', 'prod']
"""
Extend it in accordance with your conditions.

It defines valid env contexts for better IDE support when dealing with them.
- but your Editor of Choice should support it;) 
  - e.g. PyCharm support only from versions >= 2019.3
"""


import pydantic
from web_test.help.webdriver_manager import supported


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

    base_url: str = ''
    timeout: float = 6.0
    browser_name: supported.BrowserName = 'chrome'                              # todo: consider renaming to browserName for consistency with capability
    headless: bool = False
    window_width: int = 1440
    window_height: int = 900
    maximize_window: bool = False
    """
    Should be False by default, 
    because considered a bad practice 
    to write tests for not predictable window size.
    Maximized window will have different size on different machines,
    that can make tests unstable.
    """
    remote_url: Optional[str] = None
    remote_version: Optional[str] = None
    remote_platform: Optional[str] = None
    remote_enableVNC: bool = True
    remote_screenResolution: str = '1920x1080x24'
    remote_enableVideo: bool = False
    remote_enableLog: bool = True
    """
    named not in snake_case for consistency with original capability name
    """
    hold_browser_open: bool = False
    save_page_source_on_failure: bool = True
    author: str = 'yashaka'

    @classmethod
    def in_context(cls, env: Optional[EnvContext] = None) -> 'Settings':
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

from typing import Dict, Callable, Optional

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import ChromeType


from web_test.help.selenium.typing import WebDriverOptions
from . import supported

installers: Dict[
    supported.BrowserName,
    Callable[[Optional[WebDriverOptions]], WebDriver]
] = {
    supported.chrome:
        lambda opts: webdriver.Chrome(
            ChromeDriverManager().install(),
            options=opts,
        ),
    supported.chromium:
        lambda opts: webdriver.Chrome(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
            options=opts,
        ),
    supported.firefox:
        lambda opts: webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=opts,
        ),
    supported.ie:
        lambda opts: webdriver.Ie(
            IEDriverManager().install(),
            options=opts,
        ),
    supported.edge:
        lambda ____: webdriver.Edge(
            EdgeChromiumDriverManager().install(),
        ),
    supported.opera:
        lambda opts: webdriver.Opera(
            executable_path=OperaDriverManager().install(),
            options=opts,
        ),
}


def local(
        name: supported.BrowserName = 'chrome',                                 # todo: consider change default to ... and then get it from options if passed
        options: WebDriverOptions = None
) -> WebDriver:
    return installers[name](options)

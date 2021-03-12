from typing import Dict, Callable, Literal, overload

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import ChromeType

from . import supported


installers: Dict[supported.BrowserName, Callable[[], WebDriver]] = {
    supported.chrome:
        lambda: webdriver.Chrome(ChromeDriverManager().install()),
    supported.chromium:
        lambda: webdriver.Chrome(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
    supported.firefox:
        lambda: webdriver.Firefox(
            executable_path=GeckoDriverManager().install()
        ),
    supported.ie:
        lambda: webdriver.Ie(IEDriverManager().install()),
    supported.edge:
        lambda: webdriver.Edge(EdgeChromiumDriverManager().install()),
    supported.opera:
        lambda: webdriver.Opera(executable_path=OperaDriverManager().install()),
}


def driver(name: supported.BrowserName = 'chrome') -> WebDriver:
    return installers[name]()

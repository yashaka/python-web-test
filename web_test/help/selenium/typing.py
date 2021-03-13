from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import selenium

WebDriverOptions = Union[
    selenium.webdriver.ChromeOptions,
    selenium.webdriver.FirefoxOptions,
    selenium.webdriver.IeOptions,
    EdgeOptions,
    OperaOptions,
]

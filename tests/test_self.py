import config
from web_test import __version__
from web_test.test_markers import mark


pytestmark = mark.tag.fast
"""
marking all tests below as 'fast'
"""


def test_author():
    assert config.settings.author == 'yashaka'


def test_version():
    assert __version__ == '0.1.0'

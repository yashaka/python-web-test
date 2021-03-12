from typing import Callable, Optional


class Settings:                                                                 # todo: Consider even simpler impl based on dataclasses
    """
    USAGE
    =====

    from web_test.help.settings import sourced

    class Settings(sourced.Settings):

        @sourced.default(6.0)
        def timeout(self): pass

        @sourced.default(True)
        def save_page_source_on_failure(self): pass

        @sourced.default("yashaka")
        def author(self): pass


    import os
    config = Settings(
        lambda key, _: json.load(open(file)).get(key),
        os.getenv,
        # the last one takes precedence
        # you also can find some predefined sources at ./source.py
    )

    =====
    NOTES
    =====
    inspired by http://owner.aeonbits.org/docs/usage/ from Java world
    probably in Python there should be nicer ways to achieve same,
    like in pydantic, environ-config, etc.
    let's think corresponding improvement;)
    """

    def __init__(
            self,
            source: Callable[[str, Optional[str]], Optional[str]] = lambda _: None,
            *more: Callable[[str, Optional[str]], Optional[str]]
    ):
        sources = [source, *more]
        from functools import reduce
        self._source = reduce(
            (lambda f, g: lambda key, default:
             f(key, g(key, default)) if g else f(key, None)),
            sources[::-1],
            lambda _, default: default
        )

    @property
    def source(self):
        return self._source


def default(value):
    def decorator(method):

        import functools

        @functools.wraps(method)
        def fun(self: Settings):
            maybe_sourced = self.source(method.__name__, None)

            sourced_or_value = \
                maybe_sourced if maybe_sourced is not None \
                else value

            original_type = type(value)

            return original_type(sourced_or_value)

        return property(fun)

    return decorator

import functools


def pipe(*functions):
    """
    pipes functions one by one in the provided order
    i.e. applies arg1, then arg2, then arg3, and so on
    if any arg is None, just skips it
    """
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)) if g else f(x),
        functions[::-1],
        lambda x: x) if functions else None
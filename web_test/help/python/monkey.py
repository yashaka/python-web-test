# implemented based on examples from Guido van Rossum
# from https://mail.python.org/pipermail/python-dev/2008-January/076194.html


def patch_method_in(cls):
    """
    To use:
        from <somewhere> import <someclass>

        @monkey.patch_method(<someclass>)
        def <newmethod>(self, args):
            return <whatever>

    This adds <newmethod> to <someclass>
    """
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def patch_class(name, bases, namespace):
    """
    To use:

        from <somewhere> import <someclass>

        class <newclass>(<someclass>):
            __metaclass__ = monkey.patch_class
            def <method1>(...): ...
            def <method2>(...): ...
            ...

    This adds <method1>, <method2>, etc. to <someclass>, and makes
    <newclass> a local alias for <someclass>.
    """
    assert len(bases) == 1, "Exactly one base class required"
    base = bases[0]
    for name, value in namespace.iteritems():
        if name != "__metaclass__":
            setattr(base, name, value)
    return base

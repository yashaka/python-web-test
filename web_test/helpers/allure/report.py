import re
import inspect
from functools import wraps

from allure_commons import plugin_manager
from allure_commons.utils import uuid4, func_parameters, represent


def step(title):
    if callable(title):
        func = title
        name: str = title.__name__
        # todo: move to StepContext
        display_name = re.sub(r'_+', ' ', name)
        return StepContext(display_name, {})(func)
    else:
        return StepContext(title, {})


class StepContext:

    def __init__(self, title, params):
        self.title = title
        self.params = params
        self.uuid = uuid4()

    def __enter__(self):
        plugin_manager.hook.start_step(
            uuid=self.uuid,
            title=self.title,
            params=self.params)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plugin_manager.hook.stop_step(
            uuid=self.uuid,
            title=self.title,
            exc_type=exc_type,
            exc_val=exc_val,
            exc_tb=exc_tb)

    def __call__(self, func):
        @wraps(func)
        def impl(*args, **kw):
            __tracebackhide__ = True

            params = func_parameters(func, *args, **kw)
            params_values = list(params.values())
            stringified_params = ', '.join(params_values)

            def display_params():
                if not params_values:
                    return ''
                if len(params_values) == 1:
                    return ' ' + params_values[0]
                return ': ' + stringified_params

            def display_context():
                # todo: refactor naming and make idiomatic
                ismethod = lambda fn: \
                    args and inspect.getfullargspec(fn).args[0] in ['cls', 'self']

                module_name = func.__module__.split('.')[-1] \
                    if not ismethod(func) \
                    else None

                instance = args[0] if ismethod(func) else None
                instance_desc = str(instance)
                instance_name = instance_desc if not 'at 0x' in instance_desc else None
                class_name = instance and instance.__class__.__name__

                context = module_name or instance_name or class_name

                if not context:
                    return ''

                return f' [{context}]'

            name_to_display = self.title + display_params() + display_context()

            with StepContext(name_to_display, params):
                return func(*args, **kw)

            # todo: consider supporting the following original params rendering
            # with StepContext(self.title.format(*args, **params), params):
            #     return func(*args, **kw)

        return impl

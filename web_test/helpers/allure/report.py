import collections
import re
import inspect
from functools import wraps

# import allure
from allure_commons import plugin_manager
from allure_commons.utils import uuid4, represent


def _humanify(string_with_underscores, /):
    return re.sub(r'_+', ' ', string_with_underscores)                          # todo: improve ;)


def _fn_params_to_ordered_dict(func, *args, **kwargs):
    spec = inspect.getfullargspec(func)

    # given pos_or_named = list of pos_only args and pos_or_named/standard args
    pos_or_named_ordered_names = list(spec.args)
    pos_without_defaults_dict = dict(zip(spec.args, args))
    if spec.args and spec.args[0] in ['cls', 'self']:
        pos_without_defaults_dict.pop(spec.args[0], None)

    received_args_amount = len(args)
    pos_or_named_not_set = spec.args[received_args_amount:]
    pos_defaults_dict = \
        dict(zip(pos_or_named_not_set, spec.defaults or []))

    varargs = args[len(spec.args):]
    varargs_dict = \
        {spec.varargs: varargs} if (spec.varargs and varargs) else \
        {}
    pos_or_named_or_vargs_ordered_names = \
        pos_or_named_ordered_names + [spec.varargs] if varargs_dict else \
        pos_or_named_ordered_names

    pos_or_named_or_vargs_or_named_only_ordered_names = (
        pos_or_named_or_vargs_ordered_names
        + list(spec.kwonlyargs)
    )

    items = {
        **pos_without_defaults_dict,
        **pos_defaults_dict,
        **varargs_dict,
        **(spec.kwonlydefaults or {}),
        **kwargs,
    }.items()

    sorted_items = sorted(
        map(lambda kv: (kv[0], represent(kv[1])), items),
        key=
        lambda x: pos_or_named_or_vargs_or_named_only_ordered_names.index(x[0])
    )

    return collections.OrderedDict(sorted_items)


def step(title, display_params=True, display_context=True):                     # todo: add prefixes like gherkin, controlled by setting;)
    if callable(title):
        func = title
        name: str = title.__name__
        display_name = _humanify(name)                                          # todo: move to StepContext
        return StepContext(
            display_name,
            {},
            display_params=display_params,
            display_context=display_context)(func)
    else:
        return StepContext(title, {})


class StepContext:

    def __init__(self, title, params, display_params=True, display_context=True):
        self.title = title
        self.params = params
        self.uuid = uuid4()
        self.display_params = display_params
        self.display_context = display_context

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

            # params_dict = func_parameters(func, *args, **kw)
            params_dict = _fn_params_to_ordered_dict(func, *args, **kw)

            def described(item):
                (name, value) = item
                spec = inspect.getfullargspec(func)
                is_pos_or_named_passed_as_arg = \
                    name in dict(zip(spec.args, args)).keys()
                # has_defaults = spec.defaults or spec.kwonlydefaults
                # is_pos_or_named_passed_as_kwarg = \
                #     name in etc.list_intersection(spec.args, list(kw.keys()))
                return str(value) if is_pos_or_named_passed_as_arg \
                    else f'{_humanify(name)} {value}'

            params = list(map(described, list(params_dict.items())))
            params_string = ', '.join(params)
            print('params' + str(list(params)))
            params_values = list(params_dict.values())

            def params_to_display():
                if not params_values:
                    return ''
                was_fn_called_with_some_args = args or kw
                if len(params_values) == 1 and was_fn_called_with_some_args:
                    item = next(iter(params_dict.items()))
                    if item[0] in kw.keys():
                        return f' {item[0]} {item[1]}'
                    else:
                        return ' ' + params_values[0]
                return ': ' + params_string

            def context():
                # todo: refactor naming and make idiomatic
                def is_method(fn):
                    return (args
                            and
                            inspect.getfullargspec(fn)
                            .args[0] in ['cls', 'self'])

                module_name = func.__module__.split('.')[-1] \
                    if not is_method(func) \
                    else None

                instance = args[0] if is_method(func) else None
                instance_desc = str(instance)
                instance_name = \
                    instance_desc if not 'at 0x' in instance_desc \
                    else None
                class_name = instance and instance.__class__.__name__

                context_name = module_name or instance_name or class_name

                if not context_name:
                    return ''

                return f' [{context_name}]'                                     # todo: make ` [...]` configurable;)

            name_to_display = (
                    self.title
                    + (params_to_display() if self.display_params else '')
                    + (context() if self.display_context else '')
            )

            with StepContext(name_to_display, params_dict):
                return func(*args, **kw)

            # todo: consider supporting the following original params rendering
            # with StepContext(self.title.format(*args, **params), params):
            #     return func(*args, **kw)

        return impl

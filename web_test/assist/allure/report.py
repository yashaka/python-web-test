import collections
import re
import inspect
from functools import wraps, reduce

from allure_commons import plugin_manager
from allure_commons.utils import uuid4, represent


def _humanify(string_with_underscores, /):
    return re.sub(r'_+', ' ', string_with_underscores).strip()                  # todo: improve ;)


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


def step(
        title_or_callable=None,
        display_params=True,
        params_separator=', ',
        derepresent_params=False,
        display_context=True,
        translations=(),
):                                                                              # todo: add prefixes like gherkin, controlled by setting;)
    if callable(title_or_callable):
        func = title_or_callable
        name: str = title_or_callable.__name__
        display_name = _humanify(name)                                          # todo: move to StepContext
        return StepContext(
            display_name,
            {},
            display_params=display_params,
            params_separator=params_separator,
            derepresent_params=derepresent_params,
            display_context=display_context,
            translations=translations,
        )(func)
    else:
        return StepContext(
            title_or_callable,
            {},
            display_params=display_params,
            params_separator=params_separator,
            derepresent_params=derepresent_params,
            display_context=display_context,
            translations=translations,
        )


class StepContext:

    def __init__(
            self,
            title,
            params,
            display_params=True,
            params_separator=', ',
            derepresent_params=False,
            display_context=True,
            translations=(
                    (':--(', ':--)'),
                    (':--/', ':--D'),
            ),
    ):
        self.maybe_title = title
        self.params = params
        self.uuid = uuid4()
        self.display_params = display_params
        self.params_separator = params_separator
        self.derepresent_params = derepresent_params
        self.display_context = display_context
        self.translations = translations

    def __enter__(self):
        plugin_manager.hook.start_step(
            uuid=self.uuid,
            title=self.maybe_title or '',
            params=self.params)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plugin_manager.hook.stop_step(
            uuid=self.uuid,
            title=self.maybe_title or '',
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

            def derepresent(string):
                return string[1:-1]
            params_string = self.params_separator.join(
                list(map(derepresent, params)) if self.derepresent_params
                else params
            )
            params_values = list(params_dict.values())

            def title_to_display():
                return self.maybe_title or _humanify(func.__name__)

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
                return ((': ' if title_to_display() else '')
                        + params_string)

            def context():
                # todo: refactor naming and make idiomatic
                def is_method(fn):
                    spec = inspect.getfullargspec(fn)
                    return (args
                            and spec.args
                            and spec.args[0] in ['cls', 'self'])

                maybe_module_name = \
                    func.__module__.split('.')[-1] if not is_method(func) \
                    else None

                instance = args[0] if is_method(func) else None
                instance_desc = str(instance)
                maybe_instance_name = \
                    instance_desc if 'at 0x' not in instance_desc \
                    else None
                class_name = instance and instance.__class__.__name__

                context_name = maybe_module_name or maybe_instance_name or class_name

                if not context_name:
                    return ''

                return f' [{context_name}]'                                     # todo: make ` [...]` configurable;)

            name_to_display = (
                    title_to_display()
                    + (params_to_display() if self.display_params else '')
                    + (context() if self.display_context else '')
            )



            translated_name = reduce(
                lambda text, item: text.replace(item[0], item[1]),
                self.translations,
                name_to_display
            ) if self.translations else name_to_display

            with StepContext(translated_name, params_dict):
                return func(*args, **kw)

            # todo: consider supporting the following original params rendering
            # with StepContext(self.title.format(*args, **params), params):
            #     return func(*args, **kw)

        return impl

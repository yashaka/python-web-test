# MIT License
#
# Copyright (c) 2015-2021 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations


class Option:

    @staticmethod
    def in_(field) -> bool:
        return hasattr(field, 'fget') and hasattr(field.fget, 'option')

    @staticmethod
    def from_(prop) -> Option:
        return prop.fget.option

    @staticmethod
    def default(value, **attributes):
        def decorator(fun_on_self_with_request):
            option = Option(
                f'--{fun_on_self_with_request.__name__}',
                action='store',
                default=value,
                type=type(value),
                **attributes)

            def fun(self):
                return option.value(self.request)

            fun.option = option

            return property(fun)

        return decorator

    def __init__(self, name, **attributes):
        self.name = name
        self.attributes = attributes

    def value(self, from_request):
        return from_request.config.getoption(self.name)

    def register(self, parser):
        parser.addoption(self.name, **self.attributes)

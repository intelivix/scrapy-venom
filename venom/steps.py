# -*- coding: utf-8 -*-

import types
import functools

from scrapy.http import FormRequest
from scrapy.http import Request

from venom import tools


def simple_step(fn=None, timeout=5):

    def decorator(fn):
        return wrapper_factory(fn, timeout)

    def wrapper_factory(fn, timeout):
        @tools.timeout(timeout)
        @functools.wraps(fn)
        def wrapper(response):
            spider = response.meta['spider']
            kwargs = {'spider': spider, 'response': response}

            for item in fn(**kwargs) or []:
                is_function = isinstance(item, types.FunctionType)

                if isinstance(item, FormRequest) or isinstance(item, Request):
                    meta = item.meta.copy()
                    meta.update({'spider': spider})
                    yield item.replace(meta=meta)

                elif tools.is_generator(item) or is_function:
                    for item in tools.resolve_gen(item, response=response):
                        yield item
                else:
                    yield item
        return wrapper

    if fn:
        return wrapper_factory(fn, timeout)
    else:
        return decorator

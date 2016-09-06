# -*- coding: utf-8 -*-

import types
import functools

from scrapy.http import FormRequest
from scrapy.http import Request

from venom.tools import is_generator
from venom.tools import resolve_gen
from venom.tools import timeout


def simple_step(fn):

    @functools.wraps(fn)
    def wrapper(response):
        spider = response.meta['spider']
        kwargs = {
            'spider': spider,
            'response': response,
        }
        decorator = timeout(getattr(spider.timeout, 5))
        func = decorator(fn)
        for item in func(**kwargs) or []:
            if isinstance(item, FormRequest) or isinstance(item, Request):
                meta = item.meta.copy()
                meta.update({'spider': spider})
                yield item.replace(meta=meta)
            if is_generator(item) or isinstance(item, types.FunctionType):
                for item in resolve_gen(item, response=response):
                    yield item
            else:
                yield item
    return wrapper

# -*- coding: utf-8 -*-

import sys
import types
import functools
from scrapy import exceptions


def handle_exceptions(fn):

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from venom.steps.base import StepBase
        from venom.spiders import SpiderFlow
        arguments = list(args)
        self = arguments.pop(0)

        try:
            result = fn(self, *arguments, **kwargs)
            if isinstance(result, types.GeneratorType):
                result_list = []
                for item in result:
                    result_list.append(item)
                return result_list
            else:
                return result

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if issubclass(self.__class__, SpiderFlow):
                if not hasattr(self, 'venom_error'):
                    self.venom_error = (
                        exc_type, exc_value, exc_traceback)

            elif issubclass(self.__class__, StepBase):
                if not hasattr(self.spider, 'venom_error'):
                    self.spider.venom_error = (
                        exc_type, exc_value, exc_traceback)

            raise exceptions.CloseSpider(reason=str(e))

    return wrapper

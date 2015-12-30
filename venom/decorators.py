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
                if not hasattr(self, 'error'):
                    self.error = (
                        exc_type, exc_value, exc_traceback)

            elif issubclass(self.__class__, StepBase):
                if not hasattr(self.spider, 'error'):
                    self.spider.error = (
                        exc_type, exc_value, exc_traceback)

            if hasattr(e, 'msg'):
                error = e.msg
            elif hasattr(e, 'message'):
                error = e.message
            elif hasattr(e, 'reason'):
                error = e.reason
            else:
                error = 'error'

            raise exceptions.CloseSpider(reason=error)

    return wrapper

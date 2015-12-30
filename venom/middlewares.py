# -*- coding: utf-8 -*-

import sys
import importlib
import traceback
from scrapy import signals


class MiddlewareBase(object):

    def __init__(self, crawler):
        crawler.signals.connect(self.spider_closed, signals.spider_closed)
        crawler.signals.connect(self.spider_opened, signals.spider_opened)
        crawler.signals.connect(self.spider_error, signals.spider_error)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    def spider_error(self, *args, **kwargs):
        pass

    def process_spider_exception(self, response, exception, spider):
        pass


class HandleErrorsMiddleware(MiddlewareBase):

    def spider_closed(self, spider):
        if hasattr(spider, 'error'):
            traceback.print_exception(
                limit=10, file=sys.stdout, *spider.error)


class SignalHandler(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):

        handlers = crawler.settings.get('SIGNAL_HANDLERS')

        ext = cls(crawler)
        ext.spider_opened = import_handler(handlers.get('opened', None))
        ext.spider_closed = import_handler(handlers.get('closed', None))
        ext.spider_error = import_handler(handlers.get('error', None))

        if ext.spider_opened:
            crawler.signals.connect(
                ext.spider_opened, signal=signals.spider_opened)

        if ext.spider_closed:
            crawler.signals.connect(
                ext.spider_closed, signal=signals.spider_closed)

        if ext.spider_error:
            crawler.signals.connect(
                ext.spider_error, signal=signals.spider_error)

        return ext


def import_handler(func_path):

    if not func_path:
        return None

    function = func_path.split('.')[-1]
    module = '.'.join(func_path.split('.')[:-1])
    module = importlib.import_module(module)
    return getattr(module, function)

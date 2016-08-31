# -*- coding: utf-8 -*-

import errno
import os
import signal
import functools

from scrapy.exceptions import CloseSpider


def timeout(minutes=10, error_message=os.strerror(errno.ETIME), callback=None):
    def decorator(func):
        def _handler(*args, **kwargs):
            if callback:
                callback(*args, **kwargs)
            raise CloseSpider(error_message)

        def wrapper(*args, **kwargs):
            timeout_handler = functools.partial(_handler, *args, **kwargs)
            signal.signal(signal.SIGALRM, timeout_handler)
            seconds = int(minutes * 60)
            signal.alarm(seconds)
            try:
                for x in func(*args, **kwargs):
                    yield x
            finally:
                signal.alarm(0)

        return functools.wraps(func)(wrapper)
    return decorator

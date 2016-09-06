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
            signal.alarm(minutes * 60)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return functools.wraps(func)(wrapper)
    return decorator

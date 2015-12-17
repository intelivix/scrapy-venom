# -*- coding: utf-8 -*-

import types
import functools
from venom import exceptions
from venom.decorators import handle_exceptions
from venom.steps import mixins


__all__ = ['StepBase', 'InitStep']


class StepBase(object):
    """
    Base class for all steps. Implements the base functions
    and enforces the use for the BaseStep.crawl()

    """
    next_step = None

    @handle_exceptions
    def __init__(self, spider, *args, **kwargs):
        self.spider = spider
        self.parent_step = kwargs.pop('parent_step', None)
        for key, value in kwargs.iteritems():
            if not hasattr(self, key):
                raise exceptions.ArgumentError(
                    u'Attribute {} not allowed'.format(key))
            else:
                setattr(self, key, value)

    @classmethod
    def as_func(cls, spider, parent_step=None, **step_fields):
        """
        Transforms the entire class into a function

        """
        def step(*args, **kwargs):
            self = cls(
                spider=spider, parent_step=parent_step, **step_fields)

            if hasattr(self, '_init_request'):
                yield self._init_request()
            else:
                for result in self._crawl(*args, **kwargs) or []:
                    yield result

        functools.update_wrapper(step, cls, updated=())
        return step

    @handle_exceptions
    def _crawl(self, *args, **kwargs):
        """
        Method for execute before the main implementation
        (like "pre_crawl")

        """
        for result in self.crawl(*args, **kwargs) or []:
            if isinstance(result, types.GeneratorType):
                for item in result:
                    yield item
            else:
                yield result

    def crawl(self, *args, **kwargs):
        """
        The main method of the spider. This needs to be implemented
        by childs classes.

        """
        raise NotImplementedError(
            u'You must implement the method crawl()')

    def get_next_step(self):
        if hasattr(self.next_step, '__call__'):
            return self.next_step

        return self.next_step.as_func(
            spider=self.spider, parent_step=self)

    def call_next_step(self, *args, **kwargs):
        next_step_cls = kwargs.pop('next_step_cls', None)
        if next_step_cls:
            next_step = next_step_cls.as_func(
                spider=self.spider, parent_step=self)
        else:
            next_step = self.get_next_step()
        return next_step(*args, **kwargs)

    def throw_error(self, exc, exc_type, exc_value, exc_traceback):
        self.spider.venom_error = (exc_type, exc_value, exc_traceback)
        raise exc

    def response_to_file(self, path, response):
        """
        An util method for print the actual response page to
        a file specified at "path" argument

        """
        with open(path, 'wb') as f:
            f.write(response.body)


class InitStep(mixins.HttpMixin, StepBase):
    """
    Parent step required for spiders with basic flow
    such as SpiderFlow.

    Attributes:

        initial_url     URL that will be requested

    """

    initial_url = ''

    def __init__(self, *args, **kwargs):
        super(InitStep, self).__init__(*args, **kwargs)
        if not self.initial_url:
            raise exceptions.ArgumentError(
                u'You must define an initial_url')

    def _init_request(self):
        return self.dispatch(callback=self._crawl)

    def get_request_url(self):
        # Overriding the mixins.HttpMixin method
        return self.initial_url

    def crawl(self, *args, **kwargs):
        if self.next_step:
            self.call_next_step(*args, **kwargs)

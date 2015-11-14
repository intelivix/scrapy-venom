# -*- coding: utf-8 -*-

import types
import functools
from scrapy_venom import exceptions
from scrapy_venom.steps import mixins


__all__ = ['StepBase', 'InitStep']


class StepBase(object):
    """
    Base class for all steps. Implements the base functions
    and enforces the use for the BaseStep.crawl()

    """
    next_step = None

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
        def step(response=None, **context):
            self = cls(spider=spider, parent_step=parent_step, **step_fields)

            if hasattr(self, '_init_request'):
                yield self._init_request()
            else:
                for result in self._crawl(response=response, **context):
                    yield result

        functools.update_wrapper(step, cls, updated=())
        return step

    def _crawl(self, response=None, **context):
        """
        Method for execute before the main implementation
        (like "pre_crawl")

        """
        for result in self.crawl(response=response, **context) or []:
            if isinstance(result, types.GeneratorType):
                for item in result:
                    yield item
            else:
                yield result

    def crawl(self, response=None):
        """
        The main method of the spider. This needs to be implemented
        by childs classes.

        """
        raise NotImplementedError(
            u'É necessário implementar o método crawl')

    def get_next_step(self):
        return self.next_step.as_func(spider=self.spider, parent_step=self)

    def call_next_step(self, **context):
        next_step = self.get_next_step()
        return next_step(**context)


class InitStep(mixins.HttpMixin, StepBase):

    initial_url = ''

    def __init__(self, *args, **kwargs):
        super(InitStep, self).__init__(*args, **kwargs)

        if not self.initial_url:
            raise exceptions.ArgumentError(
                u'You must define an initial_url or get_request_url()')

    def _init_request(self):
        return self.dispatch(callback=self._crawl)

    def get_request_url(self):
        return self.initial_url

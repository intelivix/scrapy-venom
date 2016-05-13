# -*- coding: utf-8 -*-

from scrapy import spiders
from venom import steps
from venom import utils
from venom import exceptions
from venom.steps import generics
from venom.decorators import handle_exceptions


__all__ = ['SpiderFlow']


class SpiderFlow(spiders.Spider):
    """
    Base class for all spiders flows. Implements the base functions
    and enforces the concept of steps

    Attributes:

        name            The name of the spider
        initial_step    The initial class that will process the response
        required_args   The required args to excecute the spider
        optional_args   The optional args to excecute the spider

    """

    name = ''
    initial_step = None
    required_args = []
    optional_args = []

    def __init__(self, *args, **kwargs):
        if not issubclass(self.initial_step, steps.InitStep):
            raise exceptions.ArgumentError(
                (u'The initial_step attribute must'
                 ' be a subclass of venom.steps.InitStep'))

        self._save_required_args(kwargs)
        self._save_optional_args(kwargs)

    def _save_required_args(self, kwargs):
        for key in self.get_required_args():
            if key not in kwargs:
                raise exceptions.ArgumentError(
                    u'You must provide a argument named {}'.format(key))
            setattr(self, key, kwargs.pop(key))

    def _save_optional_args(self, kwargs):
        for key in self.get_optional_args():
            setattr(self, key, kwargs.pop(key, ''))

    @handle_exceptions
    def start_requests(self):
        initial_step = self.get_initial_step()
        for item in initial_step():
            yield item

    def get_optional_args(self):
        return self.optional_args or []

    def get_required_args(self):
        return self.required_args or []

    def get_initial_step(self):

        if not self.initial_step:
            return None

        context = self.get_initial_step_kwargs()
        return self.initial_step.as_func(**context)

    def get_initial_step_kwargs(self):
        return {
            'spider': self,
            'next_step': None,
        }


class SpiderAuthFlow(SpiderFlow):

    auth_step = None
    form_action_url = ''

    def __init__(self, *args, **kwargs):
        self._save_required_args(kwargs)
        self._save_optional_args(kwargs)

    @handle_exceptions
    def start_requests(self):
        auth_step = self.get_auth_step()
        for item in auth_step():
            yield item

    def get_auth_step(self):
        context = self.get_auth_step_kwargs()
        context.update({'spider': self})
        auth_base_cls = (self.auth_step, steps.InitStep)
        auth_cls = type(
            'InitLoginStep', auth_base_cls, {
                'form_action_url': self.form_action_url,
                'initial_url': self.form_action_url,
            })

        return auth_cls.as_func(**context)

    def get_auth_step_kwargs(self):
        return {
            'next_step': self.get_initial_step(),
        }


class SpiderSearchFlow(SpiderFlow):
    """
    Spider flow that implements the search_step at first step

    Attributes:

        initial_step    Step that will process the response from the search
        http_method     HTTP Method to request the url
        search_url      The url that will receive the request
        payload         The Query to be searched (QueryStrings or FormData)
        cookies         The Cookies of the request
        headers         The headers of the request

    """

    initial_step = None
    http_method = 'GET'
    search_step = generics.SearchStep
    payload = {}
    cookies = {}
    headers = {}

    def __init__(self, *args, **kwargs):
        self._save_required_args(kwargs)
        self._save_optional_args(kwargs)

    @handle_exceptions
    def start_requests(self):
        search_step = self.get_search_step()
        return search_step()

    def get_search_step(self):
        context = self.get_search_step_kwargs()
        context.update({'spider': self})
        search_base_cls = (self.initial_step, steps.InitStep)
        search_cls = type(
            'InitSearchStep', search_base_cls, context)

        return search_cls.as_func(**context)

    def get_search_step_kwargs(self):
        return {
            'cookies': self.get_cookies(),
            'headers': self.get_headers(),
            'payload': self.get_payload(),
            'next_step': self.initial_step,
            'initial_url': self.get_search_url(self.http_method)
        }

    def get_cookies(self):
        return self.cookies

    def get_headers(self):
        return self.headers

    def get_payload(self):
        return self.payload

    def get_search_url(self, method):

        if method == 'POST':
            return self.search_url

        return utils.make_url(
            payload=self.payload,
            url=self.search_url)

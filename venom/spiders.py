# -*- coding: utf-8 -*-

from scrapy import spiders
from venom import steps
from venom import utils
from venom import exceptions


__all__ = ['SpiderFlow']


class SpiderFlow(spiders.Spider):
    """
    Base class for all spiders flows. Implements the base functions
    and enforces the concept of steps

    Attributes:

        name            The name of the spider
        initial_step    The initial class that will process the response

    """

    name = ''
    initial_step = None

    def __init__(self, *args, **kwargs):

        if not self.name:
            self.name = utils.slugify_name(self.__class__.__name__)

        if not issubclass(self.initial_step, steps.InitStep):
            raise exceptions.ArgumentError(
                (u'The initial_step attribute must'
                 ' be a subclass of scrapy_venom.steps.InitStep'))

        super(SpiderFlow, self).__init__(*args, **kwargs)

    def start_requests(self):
        initial_step = self.get_initial_step()
        return initial_step()

    def get_initial_step(self):
        return self.initial_step.as_func(spider=self)


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
    search_url = ''
    payload = {}
    cookies = {}
    headers = {}

    def __init__(self, *args, **kwargs):
        pass

    def start_requests(self):
        search_step = self.get_search_step()
        return search_step()

    def get_search_step(self):
        context = self.get_step_context()
        context.update({'spider': self})
        search_bases_cls = (steps.InitStep,)
        search_attr = {'crawl': steps.StepBase.call_next_step}
        search_cls = type('InitSearchStep', search_bases_cls, search_attr)
        return search_cls.as_func(**context)

    def get_step_context(self):
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

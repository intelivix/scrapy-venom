# -*- coding: utf-8 -*-

from venom import exceptions
from venom.steps import mixins
from venom.steps import base


__all__ = ['SearchStep', 'SearchFlowStep']


class SearchStep(mixins.HttpMixin, base.StepBase):
    """
    Generic helper for search. After search,
    the default is pass the response to the next step

    Attributes:

        search_url     URL that will be requested

    """

    search_url = ''
    next_step = None

    def __init__(self, *args, **kwargs):
        super(SearchStep, self).__init__(*args, **kwargs)
        if not self.get_request_url():
            raise exceptions.ArgumentError(
                u'You must define an search_url or get_request_url()')

    def get_request_url(self):
        return self.search_url

    def crawl(self, response, *args, **kwargs):
        yield self.call_step(
            self.next_step, response=response)


class SearchFlowStep(SearchStep):

    def _init_request(self):
        return self.dispatch(callback=self._crawl)

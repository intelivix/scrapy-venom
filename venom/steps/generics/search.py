# -*- coding: utf-8 -*-

from venom import exceptions
from venom.steps import mixins
from venom.steps import base


__all__ = ['SearchStep']


class SearchStep(mixins.HttpMixin, base.StepBase):
    """
    Generic helper for search. After search,
    the default is pass the response to the next step

    Attributes:

        search_url     URL that will be requested

    """

    search_url = ''

    def __init__(self, *args, **kwargs):
        super(SearchStep, self).__init__(*args, **kwargs)

        if not self.search_url:
            raise exceptions.ArgumentError(
                u'You must define an search_url or get_search_url()')

    def get_request_url(self):
        return self.search_url

    def _crawl(self, *args, **kwargs):
        parent_crawl = super(SearchStep, self)._crawl
        yield self.dispatch(callback=parent_crawl)

    def crawl(self, response, *args, **kwargs):
        yield self.call_next_step(response=response)

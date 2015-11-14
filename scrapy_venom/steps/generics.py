# -*- coding: utf-8 -*-

from scrapy_venom import exceptions
from scrapy import selector as scrapy_selector
from scrapy import item as scrapy_item
from scrapy_venom.steps import mixins
from scrapy_venom.steps import base


__all__ = ['SearchStep', 'ItemStep']


class SearchStep(mixins.HttpMixin, base.StepBase):

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

    def crawl(self, response):
        yield self.call_next_step(response=response)


class ItemStep(mixins.ExtractItemMixin, base.StepBase):

    item_class = None

    def __init__(self, *args, **kwargs):
        try:
            assert self.item_class, (
                u'You must define an item_class attribute')

            assert issubclass(self.item_class, scrapy_item.Item), (
                u'The item_class must be a subclass of scrapy.Item')

        except AssertionError as e:
            raise exceptions.ArgumentError(e.message)

    def crawl(self, response=None, **context):
        result = self.get_selector(response, **context)
        for item in [x for x in result if x]:
            if isinstance(item, scrapy_selector.Selector):
                yield self.process_item(item)
            elif isinstance(item, scrapy_selector.SelectorList):
                for selector in item:
                    yield self.process_item(selector)

    def get_selector(self, response, **context):
        raise NotImplementedError(
            u'You must implement the method get_selector '
            'returning a selector or a selector list')

# -*- coding: utf-8 -*-

from scrapy import selector as scrapy_selector
from scrapy import item as scrapy_item
from venom import exceptions
from venom.steps import mixins
from venom.steps import base


__all__ = ['ItemStep']


class ItemStep(mixins.ExtractItemMixin, base.StepBase):
    """
    Generic helper for extract items from response
    You must implementate the method get_selector()
    which returns a Selector or SelectorList and
    every item will be processed in the methods

    extract_item()
    clean_item()
    build_item()

    from the mixins.ExtractItemMixin

    Attributes:

        item_class  scrapy.Item that wll be extracted from response

    """

    item_class = None

    def __init__(self, *args, **kwargs):
        super(ItemStep, self).__init__(*args, **kwargs)

        if not self.item_class:
            raise exceptions.ArgumentError(
                u'You must define an item_class attribute')

        if not issubclass(self.item_class, scrapy_item.Item):
            raise exceptions.ArgumentError(
                u'The item_class must be a subclass of scrapy.Item')

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

# -*- coding: utf-8 -*-

from scrapy import spiders
from scrapy.utils.project import get_project_settings

from venom import registry


__all__ = ['Spider']


settings = get_project_settings()


class MetaSpider(type):

    def __init__(cls, name, bases, namespace):
        super(MetaSpider, cls).__init__(name, bases, namespace)
        if hasattr(cls, 'name') and cls.name and name != 'Spider':
            if registry.spiders.find(name=cls.name):
                raise Exception(u'This spider already exists')
            registry.spiders.register(cls)


class Spider(spiders.Spider):

    name = ''
    initial_step = None
    required_args = []
    optional_args = []
    __metaclass__ = MetaSpider

    def __init__(self, *args, **kwargs):
        self._save_arguments(kwargs)
        self._save_arguments(kwargs)

    def _save_arguments(self, kwargs, required=True):
        required_args = self.get_required_args()
        optional_args = self.get_optional_args()
        cls_arguments = required_args + optional_args + ['collection_name']
        for key in cls_arguments:
            if key in required_args and key not in kwargs:
                raise Exception(u'You must provide a argument named %s' % key)
            default = 'processos' if key == 'collection_name' else None
            setattr(self, key, kwargs.get(key, default))

    def get_required_args(self):
        return self.required_args

    def get_optional_args(self):
        return self.optional_args

    def get_initial_url(self):
        return self.initial_url

    def get_initial_step(self):
        return self.initial_step

    def parse(self, response):
        initial_step = self.get_initial_step()
        response.meta['spider'] = self
        try:
            gen_step = initial_step.im_func(response)
        except AttributeError:
            gen_step = initial_step.__func__(response)

        for item in gen_step or []:
            yield item

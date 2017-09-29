# -*- coding: utf-8 -*-

import json

from scrapy import spiders
from scrapy.utils.project import get_project_settings
from constants import DEFAULT_COVERAGE, ESTADOS_BRASIL

from venom import registry


__all__ = ['Spider']


settings = get_project_settings()


class SpiderCoverage():
    self.default_coverage = DEFAULT_COVERAGE

    def check_default_coverage(self, coverage):
        return self.default_coverage == coverage

    def check_required_args(self, ):
        for arg in ['name', 'estado', 'fonte']:
            if not hasattr(cls, arg):
                return False
        return True

    def check_coverage(self):
        default_fields = DEFAULT_COVERAGE.keys()
        coverage = getattr(cls, 'coverage', {})

        coverage_fields = coverage.keys()
        if (ESTADOS_BRASIL in coverage_fields or
                'default' in coverage_fields):
            for key, value in coverage:
                sub_coverage_fields = coverage_fields
                if not set(default_fields).issubset(value):
                    return False
            return True

        elif set(default_fields).issubset(coverage_fields):
            return True
        return False

    def output_json(self):
        # TODO: adicionar argumentos dentro do coverage antes de 
        # TODO: exportar o json
        return json.dumps(getattr(cls, 'coverage', {}), ensure_ascii=False)


class MetaSpider(type):

    def __init__(cls, name, bases, namespace):
        super(MetaSpider, cls).__init__(name, bases, namespace)
        if hasattr(cls, 'name') and cls.name and name != 'Spider':
            if registry.spiders.find(name=cls.name):
                raise Exception(u'This spider already exists')
            registry.spiders.register(cls)


class Spider(spiders.Spider, SpiderCoverage):

    name = ''
    initial_step = None
    retries = 0
    required_args = []
    optional_args = []
    __metaclass__ = MetaSpider

    def __init__(self, *args, **kwargs):
        self._save_arguments(kwargs)
        self._save_arguments(kwargs)

    def _save_arguments(self, kwargs, required=True):
        required_args = self.get_required_args()
        optional_args = self.get_optional_args()
        monitor_args = self.get_monitor_args()
        cls_arguments = required_args + optional_args + monitor_args
        for key in cls_arguments:
            if key in required_args and key not in kwargs:
                raise Exception(u'You must provide a argument named %s' % key)
            setattr(self, key, kwargs.get(key, None))
        self.payload = kwargs

    def get_monitor_args(self):
        return ['job_id', 'retries']

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


class TribunaisSpider(Spider):

    default_collection_name = 'processos'

    def _save_arguments(self, kwargs, required=True):
        super(TribunaisSpider, self)._save_arguments(kwargs, required=required)
        tribunais_args = ['collection_name']
        for key in tribunais_args:
            default = self.default_collection_name if key == 'collection_name' else None  # noqa
            setattr(self, key, kwargs.get(key, default))

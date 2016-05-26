# -*- coding: utf-8 -*-

import importlib
from scrapy.utils.project import get_project_settings


def setup():
    settings = get_project_settings()
    for module in settings.get('SPIDER_MODULES'):
        importlib.import_module(module)

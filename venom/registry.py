# -*- coding: utf-8 -*-

from itertools import chain

from venom.tools.common import AttributeDict


__all__ = [
    'spiders',
    'Registry',
]


ERRORS = {
    'duplicated': '"{}" already exists!',
}


class RegistryError(Exception):
    pass


def unpack_nested_list(list_of_lists):
    return list(chain.from_iterable(list_of_lists))


def match_by_query(item, query):
    for query_key, query_value in query.items():
        item_value = getattr(item, query_key)
        if item_value != query_value:
            return False
    return True


class Registry(object):
    """Register all the modules of the application"""

    def __init__(self):
        self._modules = AttributeDict({})

    def register(self, cls):
        """Register a class into a module

        Keyword arguments:
            cls -- The class that will be registered

        """
        module = cls.__module__
        if module not in self._modules:
            self._modules[module] = []

        try:
            self._modules[module].index(cls)
            raise RegistryError(
                ERRORS['duplicated'].format(cls.__name__))

        except ValueError:
            self._modules[module].append(cls)

    def find(self, match_fn=None, **query):
        """Find a class in registry modules

        Keyword arguments:
            match_fn  -- A function that returns if the item should be included
            query     -- The query that will be executed by "match_by_query"

        """
        if match_fn:
            return self._filter_items(match_fn)
        else:
            return self._filter_items(match_by_query, query=query)

    def _filter_items(self, fn, **fn_arguments):
        """Filter objects on the modules based on "fn" argument"""
        items = []
        for item in unpack_nested_list(self._modules.values()):
            if fn(item, **fn_arguments):
                items.append(item)
        return items


spiders = Registry()

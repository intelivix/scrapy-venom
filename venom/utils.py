# -*- coding: utf-8 -*-

import re
import urllib
import unicodedata


def slugify_name(string):
    """
    Transforms a string in CammelCase in cammel_case

    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def make_url(payload, url):
    """
    Makes the url with the payload (QueryString)

    """

    if not payload:
        return url

    payload = urllib.urlencode(payload)
    url = url + '?' + payload
    return url


def get_hidden_fields(selector):
    """
    Get the hidden inputs in the response

    """
    hidden_fields = {}
    for item in selector.xpath('descendant::input[@type="hidden"]'):
        key = item.xpath('./@name').extract()[0]
        value = item.xpath('./@value').extract()
        if not value:
            value = ['']
        hidden_fields.update({key: value[0]})
    return hidden_fields


def normalize_ascii(value):
    return unicodedata.normalize('NFKD', unicode(value))\
        .encode('ascii', 'ignore')


def to_unicode(string):
    if isinstance(string, str):
        string = string.decode('utf-8')
    return string


def compare_str(str1, str2):
    str1 = to_unicode(str1).upper().strip()
    str2 = to_unicode(str2).upper().strip()
    if normalize_ascii(str1) == normalize_ascii(str2):
        return True
    else:
        return False


class _AttributeDict(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

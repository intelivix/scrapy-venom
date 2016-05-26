# -*- coding: utf-8 -*-

import unicodedata


def compare_string(str1, str2):
    pass


def get_hidden_fields(response):
    hidden_fields = {}
    for item in response.xpath('descendant::input[@type="hidden"]'):
        key = ''.join(item.xpath('./@name').extract())
        value = ''.join(item.xpath('./@value').extract())
        hidden_fields.update({key: value})
    return hidden_fields


def normalize_ascii(value):
    if isinstance(value, str):
        value = value.decode('utf-8')
    return unicodedata.normalize('NFKD', unicode(value))\
        .encode('ascii', 'ignore')

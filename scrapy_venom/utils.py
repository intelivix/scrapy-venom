# -*- coding: utf-8 -*-

import re
import urllib


def slugify_name(string):
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
        value = item.xpath('./@value').extract()[0]
        hidden_fields.update({key: value})
    return hidden_fields

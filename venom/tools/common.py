# -*- coding: utf-8 -*-

import re
import types

try:
    from urllib import urlencode
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import urlparse


def response_to_file(response, path):
    parsed_uri = urlparse(response.url)
    base_url = '%s://%s' % (parsed_uri.scheme, parsed_uri.hostname)
    html = response.body
    for script in re.findall(r'.*src="/.*', html):
        src = re.search(r'src=".*"', script).group(0).replace('src=', '').replace('"', '')  # noqa
        new_src = base_url + src
        html = html.replace(script, script.replace(src, new_src))

    with open(path, 'wb') as f:
        f.write(html)


def build_querystr(query_strings, url):
    if not query_strings:
        return url

    payload = urlencode(query_strings)
    url = url + '?' + payload
    return url


def resolve_gen(gen, *args, **kwargs):
    items = []
    for item in gen(*args, **kwargs):
        if is_generator(item):
            items += resolve_gen(item, *args, **kwargs)
        else:
            items.append(item)
    return items


def is_generator(gen):
    return isinstance(gen, types.GeneratorType)


class AttributeDict(dict):
    """Dict to act like an attribute object"""

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

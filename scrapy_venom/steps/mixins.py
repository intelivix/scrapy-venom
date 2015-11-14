# -*- coding: utf-8 -*-

from scrapy import http
from scrapy_venom import exceptions
from scrapy_venom import utils


__all__ = ['HttpMixin', 'ExtractItemMixin']


class HttpMixin(object):

    ALLOWED_METHODS = ('GET', 'POST')
    http_method = 'GET'
    request_url = ''
    payload = {}
    headers = {}
    cookies = {}

    def __init__(self, *args, **kwargs):
        super(HttpMixin, self).__init__(*args, **kwargs)

        if self.http_method not in self.ALLOWED_METHODS:
            raise exceptions.ArgumentError(
                u'This http_method is not allowed')

    def dispatch(self, callback, *args, **kwargs):
        handler = getattr(self, 'http_{}'.format(self.http_method.lower()))
        return handler(
            payload=self.get_payload(),
            cookies=self.get_cookies(),
            headers=self.get_headers(),
            request_url=self.get_request_url(),
            callback=callback)

    def http_get(self, request_url, payload, **options):
        url = utils.make_url(url=request_url, payload=payload)
        return http.Request(url=url, **options)

    def http_post(self, request_url, payload, **options):
        return http.FormRequest(url=request_url, formdata=payload, **options)

    def get_request_url(self):
        return self.request_url

    def get_payload(self):
        return self.payload

    def get_cookies(self):
        return self.cookies

    def get_headers(self):
        return self.headers


class ExtractItemMixin(object):

    def extract_item(self, selector):
        return selector.extract()

    def clean_item(self, extraction):
        return extraction or {}

    def build_item(self, cleaned_data):
        return self.item_class(**cleaned_data)

    def process_item(self, selector):
        extraction = self.extract_item(selector)
        cleaned_data = self.clean_item(extraction)
        return self.build_item(cleaned_data or {})

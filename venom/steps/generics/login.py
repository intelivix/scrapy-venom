# -*- coding: utf-8 -*-

from scrapy import http
from venom import utils
from venom import exceptions
from venom.steps import base
from venom.steps.generics import browser


__all__ = ['BrowserLoginStep', 'LoginStep']


REQUIRED_XPATHS = ['submit', 'username', 'password']
REQUIRED_CREDENTIALS = ['username', 'password']


class BrowserLoginStep(browser.BrowserStep):

    credentials = {}
    xpaths = {}
    form_action_url = ''

    def was_successfull(self, browser):
        return True

    def crawl(self, browser):
        credentials = self.get_credentials()
        xpaths = self.get_xpaths()

        browser.write(credentials['username'], xpath=xpaths['username'])
        browser.write(credentials['password'], xpath=xpaths['password'])

        button = browser.find(xpaths['submit'])
        button.click()

        if not self.was_successfull(browser):
            raise exceptions.LoginError(
                u'The authentication failed')

        if self.next_step:
            return self.call_next_step(browser)

    def get_xpaths(self):
        xpaths = self.xpaths

        for key in REQUIRED_XPATHS:
            if key not in xpaths:
                raise exceptions.ArgumentError(
                    u'You must define a "{}" key in the '
                    u'get_xpaths() method return'.format(key))
        return xpaths

    def get_credentials(self):
        credentials = self.credentials

        for key in REQUIRED_CREDENTIALS:
            if key not in credentials:
                raise exceptions.ArgumentError(
                    u'You must define a "{}" key in the '
                    u'get_credentials() method return'.format(key))
        return credentials


class LoginStep(base.StepBase):
    """
    Generic step to help in authentication

    """

    payload = {}
    form_action_url = ''

    def was_successfull(self, response):
        return True

    def crawl(self, selector):
        payload = utils.get_hidden_fields(selector)
        payload.update(self.get_payload())

        if not self.form_action_url:
            raise exceptions.ArgumentError(
                u'You must define a "form_action_url"')

        yield http.FormRequest(
            url=self.form_action_url,
            formdata=payload,
            callback=self.handle_response
        )

    def handle_response(self, response):

        if not self.was_successfull(response):
            raise exceptions.LoginError(
                u'The authentication failed')

        if self.next_step:
            return self.call_next_step(response)

    def get_payload(self):
        return self.payload

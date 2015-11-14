# -*- coding: utf-8 -*-


class Error(Exception):

    def __str__(self):
        return u'\n\033[91m>> {}\033[0m\n'.format(self.message)


class ArgumentError(Error):
    """
    Errors related with arguments

    """
    pass


class LoginError(Error):
    """
    Errors related to authentication

    """
    pass

#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-


class LocalFS:
    def __init__(self, pathname=None):
        self.path = pathname if pathname else './'

    def write(self, content, filename='default', mode='wb'):
        with open(self.path + filename, mode) as fp:
            fp.write(content)
        return self.path + filename

    def read(self, filename='default', mode='rb'):
        with open(self.path + filename, mode) as fp:
            return fp.read()

    def __str__(self):
        return 'LocalFS'


def file_storage(conf=None):
    return (conf or {}).get('__FILE_STORAGE__', LocalFS())

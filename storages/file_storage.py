#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import json


class LocalFS:
    def __init__(self, pathname=None, name=None):
        self.path = pathname if pathname else './'
        self.name = name

    def write(self, conn, content, placement='default', mode='wb'):
        if isinstance(content, dict):
            content = json.dumps(content)

        with open(self.path + placement, mode) as fp:
            fp.write(content)
        return self.path + placement

    def read(self, conn, placement='default', filtre=None, mode='rb'):
        with open(self.path + placement, mode) as fp:
            content = fp.read()
        return content

    def __str__(self):
        return self.name or 'LocalFS'


def file_storage(conf=None):
    return (conf or {}).get('__FILE_STORAGE__', LocalFS(conf.get('name')))

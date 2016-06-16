#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import os
import re
import zipfile

import click

from mongo_db import mongo_conn


def is_xml(string):
    return re.match('.*xml$', string) is not None


def parsed_pptx(pptx):
    structured_pptx = {}
    for field in pptx.namelist():
        name = field.replace('.', '\u002E')
        value = {
            'name': name,
            'value': pptx.read(field).decode('latin-1').encode('utf-8'),
            'type': 'xml' if is_xml(name) else 'media'
        }
        structured_pptx.update({name: value})
    return structured_pptx


@click.command()
@click.option('--conf', default=os.environ)
@click.option('--pptx-file', default=None)
def parse(conf, pptx_file):
    db = mongo_conn(conf)

    print 'parse pptx and store intermediate parts in mongo'

    pptx = zipfile.ZipFile(pptx_file, 'r')

    parsed_id = db.pptx.insert_one(parsed_pptx(pptx)).inserted_id

    print parsed_id
    return parsed_id


if __name__ == '__main__':
    parse()

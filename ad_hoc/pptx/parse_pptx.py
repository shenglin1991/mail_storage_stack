#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import os
import re
import zipfile

import click

from storages.mongo_db import mongo_conn


def is_xml(string):
    return re.match('.*xml$', string) is not None


def set_default_storage(db):
    db.field_to_storage.find_one_and_update({'field': 'xml'},
                                            {'$set': {
                                               'storage': {
                                                   'name': 'mongo_db',
                                                   'type': 'db'}}},
                                            upsert=True)
    db.type_to_storage.find_one_and_update({'type': 'xml'},
                                           {'$set': {
                                               'storage': {
                                                   'name': 'mongo_db',
                                                   'type': 'db'}}},
                                           upsert=True)

    db.field_to_storage.find_one_and_update({'field': 'media'},
                                            {'$set': {
                                                'storage': {
                                                    'name': 'mongo_db2',
                                                    'type': 'db'}}},
                                            upsert=True)
    db.type_to_storage.find_one_and_update({'type': 'media'},
                                           {'$set': {
                                               'storage': {
                                                   'name': 'mongo_db2',
                                                   'type': 'db'}}},
                                           upsert=True)


def parsed_pptx(pptx):
    structured_pptx = {
        'xml': {
            'name': 'xml',
            'value': [],
            'type': list.__name__
        },
        'media': {
            'name': 'media',
            'value': [],
            'type': list.__name__
        },
        'paths': {
            'name': 'paths',
            'value': '; '.join(pptx.namelist()),
            'type': str.__name__
        }
    }

    for field in pptx.namelist():
        name = field.replace('.', '\u002E')
        field_type = 'xml' if is_xml(name) else 'media'
        field_body = {
            'name': name,
            'value': pptx.read(field).decode('latin-1').encode('utf-8'),
            'type': field_type
        }
        structured_pptx[field_type]['value'].append(field_body)

    return structured_pptx


@click.command()
@click.option('--conf', default=os.environ, help='Configuration for db connexions and pptx_storage_scheme')
@click.option('--pptx-file', default=None, help='Indicate location of pptx original file')
def parse(conf, pptx_file):
    db = mongo_conn(conf)
    if not conf.get('pptx_storage_scheme'):
        set_default_storage(db)

    print 'parse pptx and store intermediate parts in mongo'

    pptx = zipfile.ZipFile(pptx_file, 'r')

    parsed_id = db.pptx.insert_one(parsed_pptx(pptx)).inserted_id

    print parsed_id
    return parsed_id


if __name__ == '__main__':
    parse()

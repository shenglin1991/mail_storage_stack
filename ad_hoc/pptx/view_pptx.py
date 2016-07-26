#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import os
import re
import time
import json
import zipfile

import click

from storages.message import redis_conn


def is_xml(string):
    return (re.match('.*xml$', string) is not None) or (re.match('.*rels$', string) is not None)


def write_pptx(name, body, pptx_file):
    name = name.replace('\u002E', '.').replace('\u2044', '/')
    body = body.encode('latin-1')
    pptx_file.writestr(name, body)


def view(db, table, _id, file_name, path=None, media_type=None):
    pptx_file = zipfile.ZipFile(file_name,
                                mode='w',
                                compression=zipfile.ZIP_DEFLATED,
                                )

    redis = redis_conn()
    structured_pptx = None
    result_subscription = redis.pubsub(ignore_subscribe_messages=True)
    result_subscription.subscribe('read_result')

    req = {
        'storage': db,
        'collection': table,
        'filtre': {
            '_id': _id
        }}

    if path:
        path = path.replace('.xml', '\u002Exml').replace('.rels', '\u002Erel').replace('/', '\u2044')
        if media_type:
            for type_name in media_type.split(','):
                path = path.replace('.' + type_name, '\u002E' + type_name)

        req.update({'projection': path})

    redis.publish('read', json.dumps(req))

    for msg in result_subscription.listen():
        structured_pptx = json.loads(msg['data']).get('result')
        break

    if structured_pptx:
        for part_type in ['xml', 'media']:
            if structured_pptx.get(part_type):
                all_parts = (structured_pptx[part_type] if isinstance(structured_pptx[part_type], list)
                             else structured_pptx[part_type]['value'])
                for part in all_parts:
                    write_pptx(part.get('name'),
                               part.get('value'),
                               pptx_file)
                structured_pptx.pop(part_type)

        if path:
            for key in structured_pptx:
                write_pptx(key.split('.', 1)[1],
                           structured_pptx.get(key),
                           pptx_file)

    pptx_file.close()
    return


@click.command()
@click.option('--id', default=None, help='stored pptx id')
@click.option('--path', help='Selection of field')
@click.option('--media-type', default='jpg,jpeg,png,gif,wmf', help='A list of recognized media type')
def main(id, conf=os.environ, path=None, media_type=None):
    file_name = conf.get('pptx_file_name', 'default.pptx')
    pptx_storage = conf.get('pptx_storage', 'mongo_db2')
    start = time.time()
    view(pptx_storage, conf.get('pptx', 'parsed_pptx'), id, file_name, path, media_type)
    print 'visual time: {}ms'.format(int((time.time() - start) * 1000))


if __name__ == '__main__':
    main()

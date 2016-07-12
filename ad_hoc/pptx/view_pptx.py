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


def view(db, table, _id, file_name, path=None):
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
        path.replace('.xml', '\u002Exml').replace('.rels', '\u002Erel')
        req.update({'projection': path})

    redis.publish('read', json.dumps(req))

    for msg in result_subscription.listen():
        structured_pptx = json.loads(msg['data']).get('result')
        break

    if structured_pptx:
        if not path or structured_pptx.get('xml'):
            for xml in structured_pptx['xml']['value']:
                name = xml.get('name').replace('\u002E', '.')
                body = xml.get('value').encode('latin-1')
                pptx_file.writestr(name, body)

        if not path or structured_pptx.get('media'):
            for media in structured_pptx['media']['value']:
                name = media.get('name').replace('\u002E', '.')
                body = media.get('value').encode('latin-1')
                pptx_file.writestr(name, body)
    pptx_file.close()
    return


@click.command()
@click.option('--id', default=None)
@click.option('--path')
def main(id, conf=os.environ, path=None):
    file_name = conf.get('pptx_file_name', 'default.pptx')
    start = time.time()
    view('mongo_db2', conf.get('pptx', 'parsed_pptx'), id, file_name, path)
    print 'visual time: {}ms'.format(int((time.time() - start) * 1000))


if __name__ == '__main__':
    main()

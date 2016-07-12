#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import json

import click

from storages.message import redis_conn


@click.command()
@click.option('--id', default=None)
@click.option('--type', default='mail', help='Type of original document: mail or pptx')
def main(id, type):
    redis = redis_conn()

    if type == 'mail':
        redis.publish('write', json.dumps({'collection': 'mails',
                                           'target_collection': 'parsed_mails',
                                           'target_storage': 'mongo_db2',
                                           'filtre': {'_id': id}}))
    elif type == 'pptx':
        redis.publish('write', json.dumps({'collection': 'pptx',
                                           'target_collection': 'parsed_pptx',
                                           'target_storage': 'mongo_db2',
                                           'filtre': {'_id': id}}))

if __name__ == '__main__':
    main()


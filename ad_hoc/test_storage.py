#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import json

import click
from bson.objectid import ObjectId

from message import redis_conn


@click.command()
@click.option('--id', default=None)
def main(id):
    redis = redis_conn()
    if id:
        _id = ObjectId(id)
    redis.publish('write', json.dumps({'collection': 'mails',
                                       'target_collection': 'parsed_mails',
                                       'target_storage': 'mongo_db2',
                                       'filtre': {'_id': str(_id)}}))

if __name__ == '__main__':
    main()


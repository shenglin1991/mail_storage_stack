#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import os
import time
import json
import webbrowser

import click

from storages.message import redis_conn
from storages.mongo_db import mongo_conn, mongo_reader


def get_body(db, body):
    body_value = ''
    # for part in body['value']:
    if isinstance(body.get('value'), list):
        for part in body.get('value'):
            part_body = mongo_reader(db, collection=part.get('collection', 'multipart'),
                                     filtre={'_id': part.get('address')})
            body_value += (get_body(db, part_body) if isinstance(part_body.get('value'), list)
                           else part_body.get('value'))
    else:
        body_value += body.get('value')
    return body_value


def view(db, mail_table, mail_id, fields):
    mail = None
    redis = redis_conn()
    result_subscription = redis.pubsub(ignore_subscribe_messages=True)
    result_subscription.subscribe('read_result')

    redis.publish('read', json.dumps({
        'storage': db,
        'collection': mail_table,
        'filtre': {
            '_id': mail_id
        }
    }))

    for msg in result_subscription.listen():
        mail = json.loads(msg['data']).get('result')
        break

    # mail = mongo_reader(db, collection=mail_table, filtre={'_id': ObjectId(mail_id)})

    if not mail:
        raise ValueError('mail not found')
    # open body in a web browser
    if 'body' in fields:
        with open('body.html', 'w') as fp:
            body = mongo_reader(db, collection='body', filtre={'_id': mail['body'].get('address')})
            fp.write(get_body(db, body).decode('utf-8').encode('latin-1'))
        webbrowser.open_new_tab('body.html')
        fields.remove('body')

    for key in fields:
        print key + ': ' + mongo_reader(db, collection=key, filtre={'_id': mail.get(key).get('address')}).get('value')


@click.command()
@click.option('--id', default=None)
@click.option('--fields', default='Subject,From,To')
def main(id, fields, conf=os.environ, db=None):
    if db is None:
        db = mongo_conn({
            '__DB_ADDR__': conf.get('__DB_ADDR__', 'localhost:27027')
        })

    start = time.time()
    view(db, conf.get('mail_table', 'parsed_mails'), id, fields.split(','))
    print 'visual time: {}ms'.format(int((time.time() - start) * 1000))


if __name__ == '__main__':
    main()

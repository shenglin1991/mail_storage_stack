#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import os
import time
import json
import webbrowser

import click

from storages.message import redis_conn


def get_body(body):
    body_value = ''
    if isinstance(body, list):
        for part in body:
            body_value += get_body(part.get('value'))
    else:
        body_value += body
    return body_value


def view(mail_storage, mail_table, mail_id, fields):
    mail = None
    redis = redis_conn()
    result_subscription = redis.pubsub(ignore_subscribe_messages=True)
    result_subscription.subscribe('read_result')

    redis.publish('read', json.dumps({
        'storage': mail_storage,
        'collection': mail_table,
        'filtre': {
            '_id': mail_id
        },
        'projection': fields
    }))

    for msg in result_subscription.listen():
        mail = json.loads(msg['data']).get('result')
        break

    if not mail:
        raise ValueError('mail not found')
    # open body in a web browser
    if 'body' in fields.split(','):
        with open('body.html', 'w') as fp:
            body = mail.get('body')
            fp.write(get_body(body).encode('latin-1'))
        webbrowser.open_new_tab('body.html')
    for key, value in mail.iteritems():
        if key != 'body':
            print key + ': ' + value


@click.command()
@click.option('--id', default=None)
@click.option('--fields', default='Subject,From,To')
def main(id, fields, conf=os.environ):
    print 'Start visualizing email'
    start = time.time()
    view('mongo_db2', conf.get('mail_table', 'parsed_mails'), id, fields)
    print 'visual time: {}ms'.format(int((time.time() - start) * 1000))


if __name__ == '__main__':
    main()

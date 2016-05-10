#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import pprint as pp

import click
from bson import ObjectId

from mongo_db import mongo_conn


@click.command()
@click.option('--id', default=None)
@click.option('--fields', default=None)
def main(id, fields):
    projection = {key: 1 for key in fields.split(',')}
    db = mongo_conn().analytics
    mail = db['new_mails'].find_one({'_id': ObjectId(id)}, projection)

    pp.pprint(mail)

if __name__ == '__main__':
    main()

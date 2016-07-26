#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import email
import os

import click

from storages.mongo_db import mongo_conn
from utils import parse_mail_to_dict


def parse_mail(filename):
    # read an email from source data
    print 'Reading mail from file'
    mail_file = open(filename, 'rb')
    mail = email.message_from_file(mail_file)
    mail_file.close()

    return parse_mail_to_dict(mail)


@click.command()
@click.option('--filename', default=None)
@click.option('--conf', default=os.environ)
def parse(filename, conf):
    db = mongo_conn(conf)

    parsed_id = db.mails.insert_one(parse_mail(filename)).inserted_id
    print 'Stored into root database: ', parsed_id
    return parsed_id


if __name__ == '__main__':
    parse()


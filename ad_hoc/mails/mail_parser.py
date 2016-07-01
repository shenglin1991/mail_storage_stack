#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import os
import email

import click

from mongo_db import mongo_conn
from utils import parse_mail_to_dict


def parse_from_str(mail_str):
    mail = email.message_from_string(mail_str)
    return parse_from_file(mail)


def parse_from_file(filename='email.eml'):
    # read an email from source data
    f = open(filename, 'rb')
    mail = email.message_from_file(f)
    f.close()

    return parse_mail_to_dict(mail)


@click.command()
@click.option('--filename', default=None)
@click.option('--mail-str', default=None)
@click.option('--conf', default=os.environ)
def parse(filename, mail_str, conf):
    db = mongo_conn(conf)

    print 'parse file or string mail'

    parsed_id = (db.mails.insert_one(parse_from_str(mail_str)).inserted_id if mail_str
                 else db.mails.insert_one(parse_from_file(filename)).inserted_id)

    print parsed_id
    return parsed_id


if __name__ == '__main__':
    parse()


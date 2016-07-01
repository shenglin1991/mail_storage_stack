#!/usr/bin/python2.7
# vim:fileencoding=utf8
# -*- coding: utf-8 -*-

import re
import itertools


def parse_content_disposition(payload):
    """
    parse content disposition and return a list of content dispositions (if there are multiple parts)
    :param payload:
    :return:
    """
    return list(itertools.chain(payload.get('Content-Disposition')
                                .translate(None, '\r\t\n')
                                .replace('; ', ';')
                                .split(';')))


def extract_name(content_type):
    """
    Get field 'name' from content_type string, in the 1st
    :param content_type:
    :return: name
    """
    content_type = (content_type.replace('; ', ';')
                    .split(';'))
    for part in content_type:
        part = part.translate(None, '\r\t\n')
        if re.search('^name', part):
            return part.split('=')[1].replace('"', '')
    return None


def unicode_payload(payload):
    # TODO : support all encodings, currently only for cp1252
    return payload.decode('latin-1').encode('utf-8')


def parse_multipart(part):
    part_info = {}

    # get a list of necessary structured information
    for key in part.keys():
        value = part.get(key)

        # parse content disposition into list
        if key == 'Content-Disposition':
            value = parse_content_disposition(part)

        part_info.update({key: value})

    is_attachment = False if part.is_multipart() else 'attachment' in part_info.get('Content-Disposition', [])

    part_info.update({'is_attachment': is_attachment})

    value = (unicode_payload(part.get_payload(decode=True)) if not part.is_multipart()
             else [parse_multipart(subpart) for subpart in part.get_payload()])

    part_info.update({'value': value})
    return part_info


def parse_mail_to_dict(mail):
    parsed_mail = {}

    # get a list of necessary structured information
    for key in mail.keys():
        value = mail.get(key)
        structured_field = {
            'name': key,
            'value': value,
            'type': type(value).__name__
        }

        parsed_mail.update({key: structured_field})

    # if payload is multipart, get extended information from content type (information are recursively extracted)
    body_value = (unicode_payload(mail.get_payload(decode=True)) if not mail.is_multipart()
                  else [parse_multipart(part) for part in mail.get_payload()])

    attachment = []
    if mail.is_multipart():
        for index, part in enumerate(body_value):
            if part.get('is_attachment', False):
                attachment.append(part)
                body_value.pop(index)

    parsed_mail.update({'body': {
        'name': 'body',
        'is_multipart': mail.is_multipart(),
        'has_attachment': len(attachment) > 0,
        'value': body_value,
        'type': type(body_value).__name__
    }})

    parsed_mail.update({'attachment': {
        'name': 'attachment',
        'value': attachment,
        'type': list.__name__
    }})

    return parsed_mail

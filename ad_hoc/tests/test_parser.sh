#!/usr/bin/env bash
export PYTHONPATH=$HOME/workspace/storage_stack/

run()
{
    python $(dirname $0)/../mails/mail_parser.py --filename=$(dirname $0)/data/example_without_attachment.eml
}

run

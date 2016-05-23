#!/usr/bin/env bash
export PYTHONPATH=$HOME/workspace/storage_stack/

run()
{
    cd $HOME/workspace/
    python mail_parser/mail_parser.py --filename=data/example.eml
}

run

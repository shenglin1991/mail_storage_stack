#!/usr/bin/env bash                                                                                                                                                                                          
export PYTHONPATH=$HOME/workspace/storage_stack/

run()
{
    cd $HOME/workspace/
    sudo python fragment_storage/store.py
}

run 

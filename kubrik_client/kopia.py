#!/usr/bin/env python3

import os
import logging


log = logging.getLogger('%s.py' % '/'.join(__name__.split('.')))

BASE_COMMAND="./kopia"


def execute_command(args):
    command = " ".join(args)
    out = os.popen(command)
    resp = out.read()    
    return resp

def validate_provider():
    """ command needs fixing"""
    return execute_command([BASE_COMMAND, "repository", "validate-provider"])

def register(gdrive_id):
    return execute_command([BASE_COMMAND, "repository", "create", "gdrive", "--folder-id="+gdrive_id, "--credentials-file",  "credentials.json"])

def connect(gdrive_id):
    """connect with gdrive id"""
    return execute_command([BASE_COMMAND, "repository", "connect", "gdrive", " --folder-id="+gdrive_id, "--credentials-file",  "credentials.json"])

def snapshot_create(local_dir):
    """start taking snapshot of a directory"""
    return execute_command([BASE_COMMAND, "snapshot", "create", local_dir])

def list_repo():
    """list all the repo which are snapshotted"""
    return execute_command([BASE_COMMAND, "snapshot", "list"])

def restore(hash_id):
    """restore the content with id right here"""
    return execute_command([BASE_COMMAND, "restore", hash_id])

def do_ls(hash_id):
    """ See content of directory"""
    return execute_command([BASE_COMMAND, "ls", "-l", id])


def move(src, dest):
    return execute_command(["mv", src, dest])


def repo_status():
    return execute_command([BASE_COMMAND, "repository", "status"])
#!/usr/bin/env python3

from distutils.command.config import config
from re import sub
from rubrik.sdk_internal.cli_tools import cli
import os
import socket
import json
import kopia
import server
import logging
import sys
from datetime import datetime

log = logging.getLogger('%s.py' % '/'.join(__name__.split('.')))

config_file = "config.txt"

def write_local_conf(config):
    f = open(config_file, "w")
    f.write(json.dumps(config))
    f.close()

def read_local_conf():
    f = open(config_file, "r")
    out = f.read()
    f.close()
    return json.loads(out)

def process_register(args):
    """    
    Server internally stores email_id and 
    uses it future communication with server
    """
    folder_id = server.register(args.email)
    config = {
        "email": args.email,
        "host": socket.gethostname(),
        "folder": folder_id
    }
    write_local_conf(config )


def process_snapshot(args):
    """
    Server uses email_id, path and passes to server, server returns response
    which fails if directory is already in snapshot
    which succeeds and returns google_drive_id
    """
    folder_id = read_local_conf().get("folder")
    kopia.snapshot_create(args.directory)
    print("process_snapshot called with arguments ", args)

def _check_valid_date(date_str):
    try:
        datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
        return True
    except Exception as e:
        return False

def list_repo():
    lst = kopia.list_repo()
    lines = lst.split("\n")
    
    key, value = '', []
    _map = {}
    for line in lines:
        line = line.strip()
        if line == '':
            _map[key] = value
            key, value = '', []
        if not _check_valid_date(line.split(" ")[0]):
            key = line
        else:
            ts = " ".join(line.split(" ")[0:3])
            hash = line.split(" ")[3]   
            value.append({"timestamp": ts, "hash": hash})
    
    return _map

def find_directory_last_known_snapshot(directory):
    _map = list_repo()
    
    for key in _map:        
        if key.endswith(directory):
            return _map[key][0]
    return None

def process_restore(args):
    """
    Server uses email_id, path and returns google_drive_id
    client and use it to navigate and figure out interaction
    """    
    snapshot_id = find_directory_last_known_snapshot(args.directory)
    if not snapshot_id:
        print("not found")
        return
    
    kopia.restore(snapshot_id)
    dirname = os.path.basename(args.directory) + "_" + snapshot_id
    kopia.move(snapshot_id, dirname)
    print("Restored to ", dirname)


def process_list_repo(args):
    _map = list_repo()
    if args.directory:
        for key in _map:
            if key.endswith(args.directory):
                print(_map[key])
    else:
        for key in _map:
            print(key)
            print(_map[key])
            print()
        
    

def parse_process_register(subparser):
    parser = cli.add_parser(
        subparser,
        'register',
        help='Register client with server',
        formatter_class=cli.Formatter,
    )
    _add_email_argument(parser)
    cli.set_defaults(parser, func=process_register)


def _add_email_argument(parser):
    cli.add_argument(
        parser,
        '-email',
        '--email',
        help='Email id of the user',
        type=str,
        required=True,
    )

def _add_directory_argument(parser, isRequired):
    cli.add_argument(
        parser,
        '-directory',
        '--directory',
        help='directory to be backed up',
        type=str,
        required=isRequired,
    )


def parse_process_snapshot(subparser):
    parser = cli.add_parser(
        subparser,
        'snapshot',
        help='Begin taking snapshot of file',
        formatter_class=cli.Formatter,
    )
    _add_directory_argument(parser, True)
    cli.set_defaults(parser, func=process_snapshot)


def parse_restore_command(subparser):
    parser = cli.add_parser(
        subparser,
        'restore',
        help='Begin restoring snapshot of a server',
        formatter_class=cli.Formatter,
    )
    _add_directory_argument(parser, True)
    cli.set_defaults(parser, func=process_restore)


def parse_list_repo(subparser):
    parser = cli.add_parser(
        subparser,
        'list',
        help='List the repo',
        formatter_class=cli.Formatter,
    )
    _add_directory_argument(parser, False)
    cli.set_defaults(parser, func=process_list_repo)

def _parse_args():
    parser = cli.create_parser(__doc__)
    subparser = cli.add_subparsers(
        parser,
        dest='op',
        help='Operation',
    )
    parse_process_register(subparser) 
    parse_process_snapshot(subparser)
    parse_restore_command(subparser)
    parse_list_repo(subparser)
    return cli.parse_args(parser)


def _main():
    args = _parse_args()
    args.func(args)    


if __name__ == '__main__':
    sys.exit(_main())

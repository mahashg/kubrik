#!/usr/bin/env python3

from distutils.command.config import config
from rubrik.sdk_internal.cli_tools import cli
import os
import socket
import json
import kopia
import server
import logging
import sys

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


def process_restore(args):
    """
    Server uses email_id, path and returns google_drive_id
    client and use it to navigate and figure out interaction
    """
    print("process_restore called with arguments ", args)


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

def _add_directory_argument(parser):
    cli.add_argument(
        parser,
        '-directory',
        '--directory',
        help='directory to be backed up',
        type=str,
        required=True,
    )


def parse_process_snapshot(subparser):
    parser = cli.add_parser(
        subparser,
        'snapshot',
        help='Begin taking snapshot of file',
        formatter_class=cli.Formatter,
    )
    _add_directory_argument(parser)
    cli.set_defaults(parser, func=process_snapshot)


def parse_restore_command(subparser):
    parser = cli.add_parser(
        subparser,
        'restore',
        help='Begin restoring snapshot of a server',
        formatter_class=cli.Formatter,
    )
    cli.set_defaults(parser, func=process_restore)


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
    return cli.parse_args(parser)


def _main():
    args = _parse_args()
    args.func(args)    


if __name__ == '__main__':
    sys.exit(_main())

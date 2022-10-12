#!/usr/bin/env python3

from rubrik.sdk_internal.cli_tools import cli
import sys
import logging


log = logging.getLogger('%s.py' % '/'.join(__name__.split('.')))


def process_register(args):
    print("process_register called with argument ", args)


def process_snapshot(args):
    print("process_snapshot called with arguments ", args)
    
def parse_process_register(subparser):
    parser = cli.add_parser(
        subparser,
        'register',
        help='Register client with server',
        formatter_class=cli.Formatter,
    )
    cli.set_defaults(parser, func=process_register)


def parse_process_snapshot(subparser):
    parser = cli.add_parser(
        subparser,
        'snapshot',
        help='Register snapshot of server',
        formatter_class=cli.Formatter,
    )
    cli.set_defaults(parser, func=process_snapshot)


def _parse_args():
    parser = cli.create_parser(__doc__)
    subparser = cli.add_subparsers(
        parser,
        dest='op',
        help='Operation',
    )
    parse_process_register(subparser) 
    parse_process_snapshot(subparser)
    return cli.parse_args(parser)


def _main():
    args = _parse_args()
    args.func(args)    



if __name__ == '__main__':
    sys.exit(_main())

#!/usr/bin/env python3

from rubrik.sdk_internal.cli_tools import cli
import sys
import logging


log = logging.getLogger('%s.py' % '/'.join(__name__.split('.')))


def process_message():
    
def _parse_args():
    parser = cli.create_parser(__doc__)
    cli.add_deployment_arguments(parser)
    cli.add_argument(
        parser,
        '-email',
        '--email',
        help='Email address whose activities need to be checked (can be substring)',
        type=str,
    )
    cli.set_defaults(parser, func=process_message)
    return cli.parse_args(parser)


def _main():
    args = _parse_args()
    log.info('This is a dry-run. No actual changes will be made as part of dry run')



if __name__ == '__main__':
    sys.exit(_main())

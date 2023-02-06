"""
SPDX-License-Identifier: MIT

Entry point for the config TUI application.
"""

import argparse
import logging

from pyfirehose.config.ui.app import ConfigApp

def main() -> int:
    """
    Main function for starting the config TUI application.
    """
    arg_parser = argparse.ArgumentParser(
        description=('Configuration file manager TUI'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    log_filename = 'logs/config.log'
    arg_parser.add_argument('-l', '--log', nargs='?', type=str, const=None, default=log_filename,
        help='log debug information to log file (can specify the full path)'
    )
    args = arg_parser.parse_args()

    logging_handlers = []
    if args.log != log_filename:
        if args.log:
            log_filename = args.log
        logging_handlers.append(logging.FileHandler(log_filename, mode='w'))

    logging.basicConfig(
        handlers=logging_handlers,
        level=logging.INFO if logging_handlers else logging.CRITICAL,
        format='%(asctime)s:T+%(relativeCreated)d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True
    )

    logging.addLevelName(logging.DEBUG, '[DEBUG]')
    logging.addLevelName(logging.INFO, '[*]')
    logging.addLevelName(logging.WARNING, '[!]')
    logging.addLevelName(logging.ERROR, '[ERROR]')
    logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

    ConfigApp().run()

    return 0

if __name__ == '__main__':
    main()

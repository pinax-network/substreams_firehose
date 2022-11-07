"""
SPDX-License-Identifier: MIT

This module is used for argument parsing and checking for the main script.
"""

import argparse
from datetime import datetime

from utils import date_to_block_num
from utils import get_auth_token

JWT = get_auth_token()

def check_period(arg_period: str) -> int:
    """
    Convert the specified period argument, from a integer or a date, to a block number.

    Args:
        arg_period:
            A period argument from the ArgumentParser.

    Returns:
        A integer representing the corresponding block number.
    """
    try:
        arg_period = int(arg_period)
    except ValueError:
        arg_period = date_to_block_num(datetime.fromisoformat(arg_period), JWT)

    if not arg_period:
        raise argparse.ArgumentTypeError(f'Invalid period: {arg_period} must be `int` or `datetime`-like object')

    return arg_period

def parse_arguments() -> argparse.Namespace:
    """
    Setup the command line interface and return the parsed arguments.

    Returns:
        A Namespace object containing the parsed arguments.
    """
    arg_parser = argparse.ArgumentParser(
        description=('Extract data from the blockchain. '
                     'Powered by Firehose (https://eos.firehose.eosnation.io/).'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument('start', type=check_period,
                            help='period start as a date (iso-like format) or a block number')
    arg_parser.add_argument('end', type=check_period,
                            help='period end as a date (iso-like format) or a block number')
    arg_parser.add_argument('-c', '--chain', choices=['eos', 'wax', 'kylin', 'jungle4'], default='eos',
                            help='target blockchain')
    arg_parser.add_argument('-o', '--out-file', type=str, default='jsonl/{chain}_{start}_to_{end}.jsonl',
                            help='output file path')
    arg_parser.add_argument('-l', '--log', nargs='?', type=str, const=None, default='logs/{datetime}.log',
                            help='log debug information to log file (can specify the full path)')
    arg_parser.add_argument('-q', '--quiet', action='store_true',
                            help='disable console logging')
    arg_parser.add_argument('-x', '--custom-exclude-expr', type=str,
                            help='custom filter for the Firehose stream to exclude transactions')
    arg_parser.add_argument('-i', '--custom-include-expr', type=str,
                            help='custom filter for the Firehose stream to tag included transactions')
    arg_parser.add_argument('-p', '--custom-processor', type=str,
                            help='relative import path to a custom block processing function located in the "block_processors" module')
    arg_parser.add_argument('--disable-signature-check', action='store_true',
                            help='disable signature checking for the custom block processing function')

    return arg_parser.parse_args()

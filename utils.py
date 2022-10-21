"""
SPDX-License-Identifier: MIT

This module provides utility functions such as querying for a block number from a date or parsing cli arguments.
"""

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timedelta

from requests_cache import CachedSession

def date_to_block_num(date: datetime, jwt: str = None) -> int:
    """
    Queries the DFUSE_GRAPHQL_ENDPOINT specified in the .env file for the block number associated with a given date time.

    Args:
        date:
            A date to retrieve the associated block number.
        jwt:
            A JWT token used for authenticating with the GraphQL API (will be fetched automatically if not specified).

    Returns:
        The block number associated with the given date time.
    """
    if not jwt:
        jwt = get_auth_token() # TODO: Catch exception

    headers = {'Authorization': f'Bearer {jwt}'}
    session = CachedSession(
        'graphql_rest',
        expire_after=timedelta(days=30),
        allowable_methods=['GET', 'POST'],
    )

    query = '''
    query ($date: Time!) {
        block: blockIDByTime(time: $date) {
            num
        }
    }
    '''

    variables = {
        'date': date.strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    data = {
        'query': query,
        'variables': variables
    }

    logging.info('Querying block number for %s...', date)

    response = session.post(os.environ.get('DFUSE_GRAPHQL_ENDPOINT'), headers=headers, data=json.dumps(data))
    block_num = 0

    if response.status_code == 200:
        logging.debug('Block number query response: %s', response.json())
        block_num = response.json()['data']['block']['num']
        logging.info('Got response: block number #%i [SUCCESS]', block_num)
    else:
        logging.warning('Could not fetch block number data (%s)', response.status_code) # TODO: Raise exception

    return block_num

def get_auth_token() -> str:
    """
    Fetch a JWT authorization token from the AUTH_ENDPOINT defined in .env. Cache the token for 24-hour use.

    Returns:
        The JWT token or an empty string if the request failed.
    """
    session = CachedSession(
        'jwt_token',
        expire_after=timedelta(days=1), # Cache JWT token (for up to 24 hours)
        allowable_methods=['GET', 'POST'],
    )

    headers = {'Content-Type': 'application/json',}
    data = f'{{"api_key":"{os.environ.get("DFUSE_TOKEN")}"}}'

    logging.info('Getting JWT token...')

    jwt = ''
    response = session.post(os.environ.get('AUTH_ENDPOINT'), headers=headers, data=data)

    if response.status_code == 200:
        logging.debug('JWT response: %s', response.json())
        jwt = response.json()['token']
        logging.info('Got JWT token (%s) [SUCCESS]', "cached" if response.from_cache else "new")
    else:
        logging.error('Could not load JWT token: %s', response.text) # TODO: Raise exception

    return jwt

def get_current_task_name() -> str:
    """
    Helper function for generating a unique task id from an asyncio task.
    """
    return asyncio.current_task().get_name()

def parse_arguments() -> argparse.Namespace:
    """
    Setup the command line interface and return the parsed arguments.

    Returns:
        A Namespace object containing the parsed arguments.
    """
    arg_parser = argparse.ArgumentParser(
        description=('Search the blockchain for transactions targeting specific accounts over a given period.'
                     'Powered by Firehose (https://eos.firehose.eosnation.io/).'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument('accounts', nargs='+', type=str,
                            help='target account(s) (single or space-separated)')
    arg_parser.add_argument('start', type=str,
                            help='period start as a date (iso-like format) or a block number')
    arg_parser.add_argument('end', type=str,
                            help='period end as a date (iso-like format) or a block number')
    arg_parser.add_argument('-c', '--chain', choices=['eos', 'wax', 'kylin', 'jungle4'], default='eos',
                            help='target blockchain')
    arg_parser.add_argument('-n', '--max-tasks', type=int, default=20,
                            help='maximum number of concurrent tasks running for block streaming')
    arg_parser.add_argument('-o', '--out-file', type=str, default='jsonl/{chain}_{accounts}_{start}_to_{end}.jsonl',
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

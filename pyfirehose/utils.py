"""
SPDX-License-Identifier: MIT

This module provides utility functions and enums for other modules.
"""

import asyncio
import json
import logging
from contextlib import nullcontext
from datetime import datetime, timedelta
from typing import Optional

from requests_cache import CachedSession

from config import Config

def date_to_block_num(date: datetime, jwt: Optional[str] = None) -> int:
    """
    Queries the DFUSE_GRAPHQL_ENDPOINT specified in the `.env` file for the block number associated with a given date time.

    Cache the results for 30 days.

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

    response = session.post(Config.GRAPHQL_ENDPOINT, headers=headers, data=json.dumps(data))
    block_num = 0

    if response.status_code == 200 and not 'errors' in response.json():
        logging.debug('Block number query response: %s', response.json())
        block_num = response.json()['data']['block']['num']
        logging.info('Got response: block number #%i [SUCCESS]', block_num)

        return block_num

    logging.warning('Could not fetch block number data: [%s] %s', response.status_code, response.json()) # TODO: Raise exception
    return 0

def get_auth_token(use_cache: bool = True) -> str:
    """
    Fetch a JWT authorization token from the authentication endpoints defined in `.env` file.

    Cache the token for 24-hour use.

    Args:
        use_cache:
            A boolean enabling/disabling fetching the cache for the JWT token request.

    Returns:
        The JWT token or an empty string if the request failed.
    """
    session = CachedSession(
        'jwt_token',
        expire_after=timedelta(days=1), # Cache JWT token (for up to 24 hours)
        allowable_methods=['GET', 'POST'],
    )

    headers = {'Content-Type': 'application/json',}
    data = f'{{"api_key":"{Config.API_KEY}"}}'

    logging.info('Getting JWT token...')

    jwt = ''
    with session.cache_disabled() if not use_cache else nullcontext():
        response = session.post(Config.AUTH_ENDPOINT, headers=headers, data=data)

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
    prefix, task_id = asyncio.current_task().get_name().rsplit('-')

    # Add leading zeroes for single digit task ids to prevent display flickering with '\r' in the console
    return f'{prefix}-{task_id.zfill(2)}'

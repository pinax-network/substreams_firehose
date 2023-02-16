"""
SPDX-License-Identifier: MIT

Functions for network related operations.
"""

import json
import logging
from contextlib import nullcontext
from datetime import datetime, timedelta

from requests_cache import CachedSession

from substreams_firehose.config.parser import Config

def date_to_block_num(date: datetime) -> int:
    """
    Query the `graphql_endpoint` specified in the main config file for the block number associated with a given date time.

    Cache the results for the duration specified in the main config file (`graphql_cache`, default is 30 days).

    Args:
        date: A date to retrieve the associated block number.

    Returns:
        The block number associated with the given date time.
    """
    jwt = get_auth_token()
    headers = {'Authorization': f'Bearer {jwt}'}
    session = CachedSession(
        'graphql_rest',
        expire_after=timedelta(days=Config.GRAPHQL_CACHE),
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

    logging.warning('Could not fetch block number data: [%s] %s', response.status_code, response.json())
    return -1

def get_auth_token(use_cache: bool = True) -> str:
    """
    Fetch a JWT authorization token from a selected authentication endpoint defined in the main config file.

    Cache the token for 24-hour use.

    Args:
        use_cache: A boolean enabling/disabling fetching the cache for the JWT token request.

    Returns:
        The JWT token.

    Raises:
        RuntimeError: If the JWT token could not be acquired from the endpoint.
    """
    session = CachedSession(
        'jwt_token',
        expire_after=timedelta(days=1), # Cache JWT token (for up to 24 hours)
        allowable_methods=['GET', 'POST'],
    )

    headers = {'Content-Type': 'application/json',}
    data = f'{{"api_key":"{Config.API_KEY}"}}'

    logging.info('Getting JWT token...')

    with session.cache_disabled() if not use_cache else nullcontext():
        response = session.post(Config.AUTH_ENDPOINT, headers=headers, data=data, timeout=10) # TODO: Make timeout part of main config

    if response.status_code == 200:
        logging.debug('JWT response: %s', response.json())
        jwt = response.json()['token']
        logging.info('Got JWT token (%s) [SUCCESS]', "cached" if response.from_cache else "new")
    else:
        logging.error('Could not load JWT token: %s', response.text)
        raise RuntimeError(f'Could not load JWT token: {json.dumps(json.loads(response.text), indent=4)}')

    return jwt

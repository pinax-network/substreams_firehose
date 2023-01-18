"""
SPDX-License-Identifier: MIT

Utility functions for other modules.
"""

import asyncio
import inspect
import importlib
import json
import logging
import os
from contextlib import nullcontext
from datetime import datetime, timedelta
from types import ModuleType
from typing import Optional

from google.protobuf.descriptor_pool import Default
from google.protobuf.descriptor_pb2 import FileDescriptorSet #pylint: disable=no-name-in-module
from google.protobuf.message_factory import GetMessages
from requests_cache import CachedSession

from pyfirehose.config.parser import Config

def date_to_block_num(date: datetime, jwt: Optional[str] = None) -> int:
    """
    Query the `graphql_endpoint` specified in the main config file for the block number associated with a given date time.

    Cache the results for the duration specified in the main config file (`graphql_cache`, default is 30 days).

    Args:
        date: A date to retrieve the associated block number.
        jwt: A JWT token used for authenticating with the GraphQL API (will be fetched automatically if not specified).

    Returns:
        The block number associated with the given date time.
    """
    if not jwt:
        jwt = get_auth_token() # TODO: Catch exception

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

    # TODO: Raise exception
    logging.warning('Could not fetch block number data: [%s] %s', response.status_code, response.json())
    return 0

def generate_proto_messages_classes(path: str = 'pyfirehose/proto/generated/protos.desc'):
    """
    Generate a mapping of services and messages full name to their class object.

    Args:
        path: Path to a descriptor set file (generated from `protoc --descriptor_set_out).

    Returns:
        A dictionary with pairs of message full name and the Python class object associated with it.

    Example:
    ```json
    {
        'dfuse.bstream.v1.BlockStream': <class 'pyfirehose.proto.generated.dfuse.bstream.v1.bstream_pb2_grpc.BlockStreamStub'>,
        'dfuse.bstream.v1.BlockStreamV2': <class 'pyfirehose.proto.generated.dfuse.bstream.v1.bstream_pb2_grpc.BlockStreamV2Stub'>,
        'dfuse.bstream.v1.BlockRequest': <class 'BlockRequest'>,
        'dfuse.bstream.v1.IrreversibleBlocksRequestV2': <class 'IrreversibleBlocksRequestV2'>,
        'dfuse.bstream.v1.BlocksRequestV2': <class 'BlocksRequestV2'>,
        'dfuse.bstream.v1.BlockResponseV2': <class 'BlockResponseV2'>,
        ...
    }
    ```
    """
    with open(path, 'rb') as proto_desc:
        descriptor_set = FileDescriptorSet.FromString(proto_desc.read())

    results = {}

    # Load service stubs objects from generated modules
    for proto_file_desc in descriptor_set.file:
        for service_name in [s.name for s in proto_file_desc.service]:
            service_key = f'{proto_file_desc.package}.{service_name}'

            for module in import_all_from_module(f'pyfirehose.proto.generated.{proto_file_desc.package}'):
                try:
                    results.update({service_key: getattr(module, f'{service_name}Stub')})
                except AttributeError:
                    pass

            if not service_key in results:
                logging.error('Could not find service stub class for "%s" in package "%s"', service_name, proto_file_desc.package)
                raise ImportError(f'Could not find service stub class for "{service_name}" in package "{proto_file_desc.package}"')

    pool = Default()

    # This needs to be separated from the previous loop in order to avoid "duplicate file name" errors
    for proto_file_desc in descriptor_set.file:
        # TODO: See if comments can be extracted without too much overhead AND if useful
        # logging.info('[PROTO_MSG] leading_comments = %s', [loc.leading_comments for loc in proto_file_desc.source_code_info.location])
        # logging.info('[PROTO_MSG] trailing_comments = %s', [loc.trailing_comments for loc in proto_file_desc.source_code_info.location])
        try:
            # Add to default pool in order to load all the messages definitions for later processing
            pool.Add(proto_file_desc)
        except TypeError:
            pass

    results.update(GetMessages(list(descriptor_set.file)))
    return results

def get_auth_token(use_cache: bool = True) -> str:
    """
    Fetch a JWT authorization token from the authentication endpoints defined in the main config file.

    Cache the token for 24-hour use.

    Args:
        use_cache: A boolean enabling/disabling fetching the cache for the JWT token request.

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

def import_all_from_module(module_name: str) -> list[ModuleType]:
    """
    Dynamically import all python files located in the specified module's folder.

    Args:
        module_name: Name of the module to import files from.

    Returns:
        The list of imported modules.
    """
    module = importlib.import_module(module_name)
    module_path = inspect.getattr_static(module, '__path__')[0]

    imported = []
    for file in os.listdir(module_path):
        if file.endswith(".py"):
            imported.append(importlib.import_module(f'{module_name}.{file.rsplit(".", 1)[0]}'))

    return imported

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
from collections.abc import Mapping, Sequence
from contextlib import nullcontext
from datetime import datetime, timedelta
from importlib.resources import is_resource, open_binary, open_text
from types import MethodType, ModuleType
from typing import BinaryIO, TextIO

from google.protobuf.descriptor_pool import Default
from google.protobuf.descriptor_pb2 import FileDescriptorSet #pylint: disable=no-name-in-module
from google.protobuf.message_factory import _FACTORY, GetMessages
from requests_cache import CachedSession

from pyfirehose.config.parser import Config

def date_to_block_num(date: datetime, jwt: str | None = None) -> int:
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

    logging.warning('Could not fetch block number data: [%s] %s', response.status_code, response.json())
    return -1

def filter_keys(input_: dict, keys_filter: dict) -> dict:
    """
    Recursively filters the `input_` dictionary based on the keys present in `keys_filter`.

    Args:
        input_: The input nested dictionary to filter.
        keys_filter: The nested dictionary filter matching subset of keys present in the `input_`.

    Returns:
        The filtered `input_` as a new dict.

    Examples:
    #### Input
    ```json
    {
        'a': 'value',
        'b': {
            'b1': 'important stuff',
            'b2': {
                'x': 'stop nesting stuff',
                'y': 'keep me !'
            }
        },
        'c': {
            'c1': [1, 2, 3],
            'c2': 'Hello'
        },
        'd': [
            {'d1': 1},
            {'d1': 2, 'd2': 3}
        ]
    }
    ```
    #### Filter
    ```json
    {
        'a': True,
        'b': {
            'b1': True,
            'b2': {
                'y': True
            }
        },
        'c': True,
        'd': {
            'd1': True,
        }
    }
    ```
    #### Output
    ```json
    {
        'a': 'value',
        'b': {
            'b1': 'important stuff',
            'b2': {
                'y': 'keep me !'
            }
        },
        'c': {
            'c1': [1, 2, 3],
            'c2': 'Hello'
        },
        'd': [
            {'d1': 1},
            {'d1': 2}
        ]
    }
    ```
    """
    output = {}
    for key, value in input_.items():
        if keys_filter == "True":
            output[key] = value
        elif key in keys_filter:
            if isinstance(value, Sequence):
                if value and isinstance(value[0], dict):
                    output[key] = [filter_keys(element, keys_filter[key]) for element in value]
                else:
                    output[key] = value
            elif isinstance(value, Mapping):
                output[key] = filter_keys(value, keys_filter[key])
            else:
                output[key] = value

    return output

def generate_proto_messages_classes(path: str = 'pyfirehose/proto/generated/protos.desc'):
    """
    Generate a mapping of services and messages full name to their class object and populates the default descriptor pool
    with the loaded `.proto` definitions.

    Should only be called once for different descriptor sets.

    Args:
        path: Path to a descriptor set file (generated from `protoc --descriptor_set_out`).

    Returns:
        A dictionary with pairs of message full name and the Python class object associated with it.

    Example:
    ```python
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
    # Save the mappings as function attribute to prevent "duplicate file name" errors when generating messages
    if not hasattr(generate_proto_messages_classes, 'saved_mappings'):
        generate_proto_messages_classes.saved_mappings = {}

    if path not in generate_proto_messages_classes.saved_mappings:
        with open_file_from_package(path, 'rb') as proto_desc:
            descriptor_set = FileDescriptorSet.FromString(proto_desc.read())

        results = {}

        # Load service stubs objects from generated modules
        for proto_file_desc in descriptor_set.file:
            for service_name in [s.name for s in proto_file_desc.service]:
                service_key = f'{proto_file_desc.package}.{service_name}'

                for module in import_all_from_module(f'pyfirehose.proto.generated.{proto_file_desc.package}'):
                    try:
                        results.update({service_key: getattr(module, f'{service_name}Stub')})
                        logging.debug('[MODULE_LOAD] Loaded %s from %s', f'{service_name}Stub', module)
                    except AttributeError:
                        pass

                if not service_key in results:
                    logging.error('Could not find service stub class for "%s" in package "%s"', service_name, proto_file_desc.package)
                    raise ImportError(f'Could not find service stub class for "{service_name}" in package "{proto_file_desc.package}"')

        pool = Default()

        # Add to default pool in separate loop in order to avoid "duplicate file name" errors when importing generated modules
        for proto_file_desc in descriptor_set.file:
            # TODO: See if comments can be extracted without too much overhead AND if useful
            # logging.info('[PROTO_MSG] leading_comments = %s', [loc.leading_comments for loc in proto_file_desc.source_code_info.location])
            # logging.info('[PROTO_MSG] trailing_comments = %s', [loc.trailing_comments for loc in proto_file_desc.source_code_info.location])
            try:
                # Add to default pool in order to load all the messages definitions for later processing
                pool.Add(proto_file_desc)
                logging.debug('[MODULE_LOAD] Added %s to default pool', proto_file_desc.name)
            except TypeError:
                logging.debug('[MODULE_LOAD] %s already in default pool', proto_file_desc.name)

        try:
            results.update(GetMessages(descriptor_set.file))
            generate_proto_messages_classes.saved_mappings[path] = results
            logging.debug('[MODULE_LOAD] Saved mappings for file "%s"', path)
        except TypeError as error:
            # Saved mappings should prevent this error to ever show up
            logging.error('Symbol already loaded in default descriptor pool : %s', error)
            raise ImportError from error

        return results

    return generate_proto_messages_classes.saved_mappings[path]

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

def open_file_from_package(path: str, mode: str = 'r') -> BinaryIO | TextIO:
    """
    Open a file (read-only) located in the package install directory using its relative path.
    If the file is not a valid resource, try to open it in the current directory.

    Args:
        path: Relative path of the resource inside the package install directory or local path.
        mode: One of `r` (text) or `rb` (binary).

    Returns:
        A text or binary stream to use in a `with` statement.

    Raises:
        FileNotFoundError: If the file specified by `path` doesn't exists.
        IsADirectoryError: If the file specified by `path` is a directory.
        ValueError: If the `mode` argument is not one of `r` or `rb`.
    """
    if mode not in ['r', 'rb']:
        raise ValueError('`mode` argument must be one of `r` (text) or `rb` (binary).')

    if not '/' in path:
        path = f'./{path}'

    package, resource = path.rsplit('/', 1)
    package = package.replace('/', '.')

    try:
        if is_resource(package, resource):
            return open_text(package, resource, encoding='utf8') if mode == 'r' else open_binary(package, resource)
    except TypeError:
        pass

    return open(path, mode, encoding='utf8') if mode == 'r' else open(path, mode)

def patch_get_messages(self, files):
    """
    THIS IS A PATCHED FUNCTION FROM THE GOOGLE PROTOBUF LIBRARY. ORIGINAL DOCUMENTATION FOLLOWS.

    Gets all the messages from a specified file.

    This will find and resolve dependencies, failing if the descriptor
    pool cannot satisfy them.

    Args:
    files: The file names to extract messages from.

    Returns:
    A dictionary mapping proto names to the message classes. This will include
    any dependent messages as well as any messages defined in the same file as
    a specified message.
    """
    result = {}
    for file_name in files:
        file_desc = self.pool.FindFileByName(file_name)
        for desc in file_desc.message_types_by_name.values():
            result[desc.full_name] = self.GetPrototype(desc)

    # While the extension FieldDescriptors are created by the descriptor pool,
    # the python classes created in the factory need them to be registered
    # explicitly, which is done below.
    #
    # The call to RegisterExtension will specifically check if the
    # extension was already registered on the object and either
    # ignore the registration if the original was the same, or raise
    # an error if they were different.

    for extension in file_desc.extensions_by_name.values():
        if extension.containing_type not in self._classes: #pylint: disable=protected-access
            self.GetPrototype(extension.containing_type)
        extended_class = self._classes[extension.containing_type] #pylint: disable=protected-access

        # === Patch starts here ===

        # Catch the exception from `RegisterExtension` to prevent `NotImplementedError` breaking the *whole* loop.
        try:
            extended_class.RegisterExtension(extension)
        except NotImplementedError:
            pass

        # === Patch ends here ===

        if extension.message_type:
            self.GetPrototype(extension.message_type)
    return result

# Monkey-patching the `GetMessages` function to prevent `NotImplementedError` exceptions
_FACTORY.GetMessages = MethodType(patch_get_messages, _FACTORY)

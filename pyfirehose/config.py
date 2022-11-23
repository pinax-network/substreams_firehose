"""
SPDX-License-Identifier: MIT

This module ...
"""

import inspect
import importlib
import logging
import os
from dataclasses import dataclass
from typing import Any, ClassVar

# https://hjson.github.io/hjson-py/ -- allow comments in JSON files for configuration purposes
import hjson

@dataclass
class StubConfig:
    REQUEST_OBJECT: ClassVar[Any]
    REQUEST_PARAMETERS: ClassVar[dict]
    STUB_OBJECT: ClassVar[Any]

@dataclass
class Config:
    API_KEY: ClassVar[str]
    AUTH_ENDPOINT: ClassVar[str]
    CHAIN: ClassVar[str]
    GRAPHQL_ENDPOINT: ClassVar[str]
    GRPC_ENDPOINT: ClassVar[str]
    MAX_BLOCK_SIZE: ClassVar[int]

def import_all_from_module(module_name: str):
    module = importlib.import_module(module_name)
    module_path = inspect.getattr_static(module, '__path__')[0]

    imported = []
    for file in os.listdir(module_path):
        if file.endswith(".py"):
            imported.append(importlib.import_module(f'{module_name}.{file.rsplit(".", 1)[0]}'))

    return imported

def load_config(file: str):
    with open(file, 'r', encoding='utf8') as config_file:
        try:
            options = hjson.load(config_file)
        except hjson.HjsonDecodeError as error:
            logging.exception('Error decoding main config file (%s): %s', file, error)
            raise

    try:
        default_grpc = options['grpc'][options['default']]
        default_auth = options['auth'][default_grpc['auth']]
        default_stub = default_grpc['stub']

        Config.API_KEY 			= default_auth['api_key']
        Config.AUTH_ENDPOINT 	= default_auth['endpoint']
        Config.CHAIN 			= default_grpc['chain']
        Config.GRAPHQL_ENDPOINT = options['graphql_endpoint']
        Config.GRPC_ENDPOINT 	= default_grpc['url']
        Config.MAX_BLOCK_SIZE 	= options['max_block_size']
    except KeyError as error:
        logging.exception('Error parsing main config file (%s): %s', file, error)
        raise

    logging.debug('Loaded main config: %s [SUCCESS]', vars(Config))

    stub_config = default_stub
    # Load stub config from external file
    if isinstance(default_stub, str):
        with open(default_stub, 'r', encoding='utf8') as stub_config_file:
            try:
                stub_config = hjson.load(stub_config_file)
            except hjson.HjsonDecodeError as error:
                logging.exception('Error decoding stub config file (%s): %s', default_stub, error)
                raise

    try:
        import_dir_module = f'proto.generated.{stub_config["python_import_dir"]}'
        imported = import_all_from_module(import_dir_module)

        for module in imported:
            try:
                StubConfig.STUB_OBJECT = getattr(module, f'{stub_config["name"]}Stub')
            except AttributeError:
                pass

            try:
                StubConfig.REQUEST_OBJECT = getattr(module, stub_config['request'])
            except AttributeError:
                pass

        if not StubConfig.STUB_OBJECT:
            logging.critical('Could not load stub object from config: unable to locate "%sStub" in "%s" module',
                stub_config['name'],
                f'proto.generated.{stub_config["python_import_dir"]}')
            raise Exception

        if not StubConfig.REQUEST_OBJECT:
            logging.critical('Could not load request object from config: unable to locate "%s"', stub_config['request'])
            raise Exception

        StubConfig.REQUEST_PARAMETERS = {}
        for key, value in stub_config['parameters'].items():
            StubConfig.REQUEST_PARAMETERS[key] = value
    except ImportError as error:
        logging.exception('Error importing modules from specified directory (%s): %s',
            stub_config['python_import_dir'],
            error
        )
        raise
    except KeyError as error:
        logging.exception('Error parsing stub config (%s): %s', stub_config, error)
        raise

    logging.debug('Loaded stub config: %s [SUCCESS]', vars(StubConfig))

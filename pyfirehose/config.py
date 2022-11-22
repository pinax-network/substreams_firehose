"""
SPDX-License-Identifier: MIT

This module ...
"""

import logging
from dataclasses import dataclass
from typing import ClassVar

# https://hjson.github.io/hjson-py/ -- allow comments in JSON files for configuration purposes
import hjson

@dataclass
class Config:
    API_KEY: ClassVar[str]
    AUTH_ENDPOINT: ClassVar[str]
    CHAIN: ClassVar[str]
    GRAPHQL_ENDPOINT: ClassVar[str]
    GRPC_ENDPOINT: ClassVar[str]
    MAX_BLOCK_SIZE: ClassVar[int]

def load_config(file: str):
    with open(file, 'r', encoding='utf8') as config_file:
        try:
            options = hjson.load(config_file)
        except hjson.HjsonDecodeError as error:
            logging.exception('Error decoding config file (%s): %s', file, error)
            raise

        try:
            Config.API_KEY = options['auth']['eosnation']['api_key']
            Config.AUTH_ENDPOINT = options['auth']['eosnation']['endpoint']
            Config.GRAPHQL_ENDPOINT = options['graphql_endpoint']
            Config.MAX_BLOCK_SIZE = options['max_block_size']

            grpc_option = options['grpc'][0] # TODO: Make this selectable / default value
            Config.CHAIN = grpc_option['chain']
            Config.GRPC_ENDPOINT = grpc_option['url']
        except KeyError as error:
            logging.exception('Error parsing config file (%s): %s', file, error)
            raise

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
            default_grpc = options['grpc'][options['default']['grpc']]
            default_auth = options['auth'][default_grpc['auth']]

            Config.API_KEY 			= default_auth['api_key']
            Config.AUTH_ENDPOINT 	= default_auth['endpoint']
            Config.CHAIN 			= default_grpc['chain']
            Config.GRAPHQL_ENDPOINT = options['graphql_endpoint']
            Config.GRPC_ENDPOINT 	= default_grpc['url']
            Config.MAX_BLOCK_SIZE 	= options['max_block_size']
        except KeyError as error:
            logging.exception('Error parsing config file (%s): %s', file, error)
            raise

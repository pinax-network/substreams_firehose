"""
SPDX-License-Identifier: MIT

This module provides a default block processor for *Firehose v2* supported chains.
"""
import logging

from google.protobuf.message import Message

from pyfirehose.proto.generated.sf.antelope.type.v1 import type_pb2

def default_block_processor(raw_block: Message) -> dict:
    logging.debug('Data: %s', raw_block)
    yield {}

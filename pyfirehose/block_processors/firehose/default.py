"""
SPDX-License-Identifier: MIT

This module ...
"""
import logging

from google.protobuf.message import Message

from proto.generated.sf.antelope.type.v1 import type_pb2

def eos_block_processor(raw_block: Message) -> dict:
    block = type_pb2.Block()
    raw_block.Unpack(block)

    logging.debug(block)
    yield {}

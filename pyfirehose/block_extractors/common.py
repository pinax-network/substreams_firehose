"""
SPDX-License-Identifier: MIT

This module holds common functions used by the block extractors.
"""

import logging
from collections.abc import Generator
from contextlib import asynccontextmanager
from typing import Callable, Optional, Sequence

import grpc
from google.protobuf.message import Message

from config import Config, StubConfig
from exceptions import BlockStreamException
from utils import get_auth_token
from utils import get_current_task_name

@asynccontextmanager
async def get_secure_channel() -> Generator[grpc.aio.Channel, None, None]:
    """
    Instantiate a secure gRPC channel as an asynchronous context manager used by block extractors.

    Yields:
        A grpc.aio.Channel as an asynchronous context manager.
    """
    jwt = get_auth_token()
    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(jwt)
    )

    yield grpc.aio.secure_channel(
        Config.GRPC_ENDPOINT,
        creds,
        # See https://github.com/grpc/grpc/blob/master/include/grpc/impl/codegen/grpc_types.h#L141 for a list of options
        options=[
            ('grpc.max_receive_message_length', Config.MAX_BLOCK_SIZE), # default is 8MB
            ('grpc.max_send_message_length', Config.MAX_BLOCK_SIZE), # default is 8MB
        ],
        compression=Config.COMPRESSION
    )

def process_blocks(raw_blocks: Sequence[Message], block_processor: Callable[[Message], dict]) -> list[dict]:
    """
    Parse data using the given `block_processor` from previously extracted raw blocks into a file.

    Args:
        raw_blocks:
            A sequence of packed blocks (google.protobuf.any_pb2.Any objects) extracted from Firehose.
        block_processor:
            A generator function extracting relevant properties from a block.

    Returns:
        The list of parsed information.
    """
    data = []
    for raw_block in raw_blocks:
        for blob in block_processor(raw_block):
            data.append(blob)

    logging.info('Finished block processing, parsed %i rows of data [SUCCESS]', len(data))

    return data

async def stream_blocks(start: int, end: int, secure_channel: grpc.aio.Channel, #pylint: disable=too-many-arguments
                        block_processor: Optional[Callable[[Message], dict]] = None, **kwargs) -> list[Message | dict]:
    """
    Return raw blocks (or parsed data) for the subset period between `start` and `end` using the provided filters.

    Args:
        start:
            The stream's starting block.
        end:
            The stream's ending block.
        secure_channel:
            The gRPC secure channel (SSL/TLS) to fetch block from the Firehose endpoint.
        custom_include_expr:
            A custom Firehose filter for tagging blocks as included.
        custom_exclude_expr:
            A custom Firehose filter for excluding blocks from the results.
        block_processor:
            Optional block processor function for directly parsing raw blocks.
            The function will then return the parsed blocks instead.

            Discouraged as it might cause congestion issues for the gRPC channel if the block processing takes too long.
            Parsing the blocks *after* extraction allows for maximum throughput from the block stream.

    Returns:
        A list of raw blocks (google.protobuf.any_pb2.Any objects) or parsed data if a block processor is supplied.

    Raises:
        BlockStreamException:
            If an rpc error is encountered. Contains the start, end, and failed block number.
    """
    data = []
    current_block_number = start
    stub = StubConfig.STUB_OBJECT(secure_channel)
    # Move request parameters to dict to allow CLI keyword argument to override the stub config
    request_parameters = {
        'start_block_num': start,
        'stop_block_num': end,
        **StubConfig.REQUEST_PARAMETERS,
        **kwargs
    }

    logging.debug('[%s] Starting streaming blocks from #%i to #%i...',
        get_current_task_name(),
        start,
        end,
    )

    try:
        # Duplicate code for moving invariant out of loop, preventing condition check on every block streamed
        if block_processor:
            async for response in stub.Blocks(StubConfig.REQUEST_OBJECT(**request_parameters)): #pylint: disable=no-member
                logging.debug('[%s] Getting block number #%i (%i blocks remaining)...',
                    get_current_task_name(),
                    current_block_number,
                    end - current_block_number
                )

                current_block_number += 1

                for blob in block_processor(response.block):
                    data.append(blob)
        else:
            async for response in stub.Blocks(StubConfig.REQUEST_OBJECT(**request_parameters)): #pylint: disable=no-member
                logging.debug('[%s] Getting block number #%i (%i blocks remaining)...',
                    get_current_task_name(),
                    current_block_number,
                    end - current_block_number
                )

                current_block_number += 1
                data.append(response.block)
    except grpc.aio.AioRpcError as error:
        logging.error('[%s] Failed to process block number #%i: %s',
            get_current_task_name(),
            current_block_number,
            error
        )

        raise BlockStreamException(start, end, current_block_number) from error

    logging.debug('[%s] Done !\n', get_current_task_name())
    return data

"""
SPDX-License-Identifier: MIT
"""

import json
import logging
import os
import os.path
from typing import Callable, Dict, List, Sequence

import grpc
from google.protobuf.message import Message

from exceptions import BlockStreamException
from proto import bstream_pb2
from proto import bstream_pb2_grpc
from proto import codec_pb2
from utils import get_current_task_name

async def stream_blocks(start: int, end: int, secure_channel, custom_include_expr, custom_exclude_expr) -> List[Message]:
    """
    Return a subset of transactions for blocks between `start` and `end` using the provided filters.

    Args:
        start:
            The stream's starting block.
        end:
            The stream's ending block.

    Returns:
        A list of raw blocks (google.protobuf.any_pb2.Any objects).
    """
    raw_blocks = []
    current_block_number = start
    stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)

    logging.debug('[%s] Starting streaming blocks from #%i to #%i...',
        get_current_task_name(),
        start,
        end,
    )

    try:
        async for response in stub.Blocks(bstream_pb2.BlocksRequestV2( #pylint: disable=no-member
            start_block_num=start,
            stop_block_num=end,
            fork_steps=['STEP_IRREVERSIBLE'],
            include_filter_expr=custom_include_expr,
            exclude_filter_expr=custom_exclude_expr
        )):
            logging.debug('[%s] Getting block number #%i (%i blocks remaining)...',
                get_current_task_name(),
                current_block_number,
                end - current_block_number
            )

            current_block_number += 1
            raw_blocks.append(response.block)
    except grpc.aio.AioRpcError as error:
        logging.error('[%s] Failed to process block number #%i: %s',
            get_current_task_name(),
            current_block_number,
            error
        )

        raise BlockStreamException(start, end, current_block_number) from error

    logging.debug('[%s] Done !\n', get_current_task_name())
    return raw_blocks

def process_blocks(raw_blocks: Sequence[Message], block_processor: Callable[[codec_pb2.Block], Dict],
                   out_file: str) -> int:
    """
    Parse data using the given `block_processor` from previously extracted raw blocks into a file.

    Args:
        raw_blocks:
            A sequence of packed blocks (google.protobuf.any_pb2.Any objects) extracted from Firehose.
        block_processor:
            A generator function extracting relevant properties from a block.
        out_file:
            The path or filename for the output data file.

    Returns:
        An integer indicating the success/failure status.
    """
    data = []
    for raw_block in raw_blocks:
        block = codec_pb2.Block()
        raw_block.Unpack(block)
        for transaction in block_processor(block):
            data.append(transaction)

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w', encoding='utf8') as out:
        for entry in data:
            json.dump(entry, out) # TODO: Add exception handling
            out.write('\n')

    logging.info('Finished block processing, wrote %i rows of data to %s [SUCCESS]',
        len(data),
        out_file
    )

    return 0

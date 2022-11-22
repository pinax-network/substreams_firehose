"""
SPDX-License-Identifier: MIT

This extractor is the first to separate the block streaming process from the block processing, preventing any bottleneck
coming from the parsing of the raw data. This allows for an increased throughput as only raw blocks are extracted from
the gRPC stream.

It uses asynchronous directives to divide the work into a *fixed* amount of workers defined by the `initial_tasks`
argument. If a task fails, it waits for all the other tasks to finish before restarting the failed task again for
the missing blocks.

Diagram: see 'asynchronous_optimized_block_streaming.jpg'
"""

import asyncio
import logging

from google.protobuf.message import Message

from block_extractors.common import get_secure_channel
from block_extractors.common import stream_blocks
from config import Config
from exceptions import BlockStreamException

async def asyncio_main(period_start: int, period_end: int, initial_tasks: int = 25, #pylint: disable=too-many-arguments
                       custom_include_expr: str = '', custom_exclude_expr: str = '') -> list[Message]:
    """
    Extract blocks from a Firehose endpoint as raw blocks for later processing.

    Using asynchronous directives, a *fixed* amount of workers will be initially spawned to
    extract data from the gRPC channel until all blocks have been retrieved.
    The returned list can then be parsed for extracting relevant data from the blocks.

    Args:
        period_start:
            The first block number of the targeted period.
        period_end:
            The last block number of the targeted period.
        initial_tasks:
            The initial number of concurrent tasks to start for streaming blocks.
        custom_include_expr:
            A custom Firehose filter for tagging blocks as included.
        custom_exclude_expr:
            A custom Firehose filter for excluding blocks from the results.

    Returns:
        A list of raw blocks (google.protobuf.any_pb2.Any objects) that can later be processed.
    """
    block_diff = period_end - period_start
    # Prevent having more tasks than the amount of blocks to process
    split = block_diff//initial_tasks if block_diff > initial_tasks else block_diff

    logging.info('Streaming %i blocks on %s chain (running %i workers)...',
        period_end - period_start,
        Config.CHAIN,
        initial_tasks
    )

    tasks = set()
    data = []
    async with get_secure_channel() as secure_channel:
        for i in range(initial_tasks):
            tasks.add(
                asyncio.create_task(
                    stream_blocks(
                        period_start + i*split,
                        # Gives the remaining blocks to the last task in case the work can't be splitted equally
                        period_start + (i+1)*split - 1 if i < initial_tasks-1 else period_end,
                        secure_channel,
                        custom_include_expr,
                        custom_exclude_expr
                    )
                )
            )

        failed_tasks = tasks.copy()
        while failed_tasks:
            failed_tasks.clear()
            for task in tasks:
                try:
                    data += await task
                except BlockStreamException as error:
                    failed_tasks.add(
                        asyncio.create_task(
                            stream_blocks(error.failed, error.end, secure_channel, custom_include_expr, custom_exclude_expr)
                        )
                    )

            tasks = failed_tasks.copy()

    logging.info('Block streaming done !')
    return data

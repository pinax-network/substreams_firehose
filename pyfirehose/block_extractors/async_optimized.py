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

from pyfirehose.block_extractors.common import get_secure_channel
from pyfirehose.block_extractors.common import stream_blocks
from pyfirehose.config.utils import Config
from pyfirehose.exceptions import BlockStreamException

async def asyncio_main(period_start: int, period_end: int, initial_tasks: int = 25, **kwargs) -> list[Message]:
    """
    Extract blocks from a gRPC channel as raw blocks for later processing.

    Using asynchronous directives, a *fixed* amount of workers will be initially spawned to
    extract data from the gRPC channel until all blocks have been retrieved.
    The returned list can then be parsed for extracting relevant data from the blocks.

    Args:
        period_start: The first block number of the targeted period.
        period_end: The last block number of the targeted period.
        initial_tasks: The initial number of concurrent tasks to start for streaming blocks.
        kwargs: Additional keyword arguments to pass to the gRPC request (must match .proto file definition).

    Returns:
        A list of raw blocks (google.protobuf.any_pb2.Any objects) that can later be processed.
    """
    block_diff = period_end - period_start
    split = block_diff//initial_tasks

    # Prevent having more tasks than the amount of blocks to process
    if block_diff <= initial_tasks:
        split = block_diff
        initial_tasks = 1

    logging.info('Streaming %i blocks on %s chain (running %i workers)...',
        period_end - period_start + 1,
        Config.CHAIN,
        initial_tasks
    )

    tasks = set()
    data = []
    failed_counter = {}
    async with get_secure_channel() as secure_channel:
        for i in range(initial_tasks):
            tasks.add(
                asyncio.create_task(
                    stream_blocks(
                        period_start + i*split,
                        # Gives the remaining blocks to the last task in case the work can't be splitted equally
                        period_start + (i+1)*split - 1 if i < initial_tasks-1 else period_end,
                        secure_channel,
                        **kwargs
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
                    failed_counter[error.failed] = failed_counter.get(error.failed, 0) + 1
                    if failed_counter[error.failed] <= Config.MAX_FAILED_BLOCK_RETRIES:
                        logging.warning('Could not fetch block #%i: retrying... (%i/%i retries)',
                            error.failed,
                            failed_counter[error.failed],
                            Config.MAX_FAILED_BLOCK_RETRIES
                        )

                        failed_tasks.add(
                            asyncio.create_task(
                                stream_blocks(error.failed, error.end, secure_channel, **kwargs)
                            )
                        )
                    else:
                        logging.error('Could not fetch block #%i: maximum number of retries reached (%i)',
                            error.failed,
                            Config.MAX_FAILED_BLOCK_RETRIES
                        )

            tasks = failed_tasks.copy()

    logging.info('Block streaming done !')
    return data

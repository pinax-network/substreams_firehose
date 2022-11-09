"""
SPDX-License-Identifier: MIT

This extractor differs from `async_optimized` by scaling automatically the number of workers needed according to the
`workload` parameter. Each task will extract a fixed amount of raw blocks and a 'spawner' task will periodically spawn
new workers until the block pool (remaining blocks that need to be fetched) is empty.

The 'spawner' task will first max out the number of workers for a *single* channel (25 is the stable value that seems
to hold for every execution of the program) and only spawn new workers if the number falls below the established maximum
(and the block pool isn't already empty).

Diagram: see 'asynchronous_optimized_block_streaming.jpg'
"""

import asyncio
import logging
import statistics
import time

from google.protobuf.message import Message

#pylint: disable=wrong-import-position
from block_extractors.common import get_secure_channel
from block_extractors.common import stream_blocks
from exceptions import BlockStreamException
from utils import get_current_task_name
#pylint: enable=wrong-import-position

async def asyncio_main(period_start: int, period_end: int, chain: str = 'eos', #pylint: disable=too-many-arguments, too-many-locals, too-many-statements
              initial_tasks: int = 25, workload: int = 100, auto_adjust_frequency: bool = False, spawn_frequency: float = 0.1,
              custom_include_expr: str = '', custom_exclude_expr: str = '') -> list[Message]:
    """
    Extract blocks from a Firehose endpoint as raw blocks for later processing.

    Using asynchronous directives, a number of workers will be periodically spawned to
    extract data from the gRPC channel until all blocks have been retrieved.
    The returned list can then be parsed for extracting relevant data from the blocks.

    Args:
        period_start:
            The first block number of the targeted period.
        period_end:
            The last block number of the targeted period.
        chain:
            The target blockchain determining the Firehose endpoint used for streaming blocks.
        initial_tasks:
            The initial number of concurrent tasks to start for streaming blocks.
        workload:
            The number of blocks to extract for each task.
        auto_adjust_frequency:
            Enable the task spawner to auto adjust the task spawning frequency based on the tasks' average runtime.
        spawn_frequency:
            The sleep time (in seconds) for the spawner to wait before trying to spawn a new task.
            Will be overridden if `auto_adjust_frequency` is enabled.
        custom_include_expr:
            A custom Firehose filter for tagging blocks as included.
        custom_exclude_expr:
            A custom Firehose filter for excluding blocks from the results.

    Returns:
        A list of raw blocks (google.protobuf.any_pb2.Any objects) that can later be processed.
    """
    async def _spawner():
        """
        Periodically try to spawn new workers for extracting blocks until the block pool is empty.
        """
        def __task_done_callback(task):
            """
            When a task is done, remove the task from the `running` set and add it to the `done` queue.
            """
            if task.exception():
                logging.error('%s encountered an exception', task.get_name())
            else:
                logging.debug('%s finished block streaming', task.get_name())
            tasks_running.remove(task)
            tasks_done.put_nowait(task)

        while True:
            logging.debug('[%s] %i tasks running | polling every %fs | %i blocks remaining in block pool',
                get_current_task_name(),
                len(tasks_running),
                spawn_frequency,
                len(block_pool) * workload,
            )

            try:
                await asyncio.sleep(spawn_frequency)
            except asyncio.CancelledError:
                logging.warning('[%s] Cancelled, stopping spawner task NOW...', get_current_task_name())
                return

            if not block_pool:
                logging.warning('[%s] No more blocks in block pool, stopping spawner task NOW...',
                    get_current_task_name(),
                )
                return

            if (max_tasks and len(tasks_running) >= max_tasks):
                continue

            new_task = asyncio.create_task(
                stream_blocks(
                    *block_pool.pop(),
                    secure_channel,
                    custom_include_expr,
                    custom_exclude_expr
                )
            )
            new_task.add_done_callback(__task_done_callback)
            tasks_running.add(new_task)

    block_diff = period_end - period_start
    # Run only one task if number of block to stream is very small
    if block_diff < initial_tasks:
        initial_tasks = 1
        workload = block_diff
    # Adjust workload to give work to all the tasks in case the number of blocks to stream is too small
    elif block_diff < initial_tasks * workload:
        workload = block_diff//initial_tasks

    tasks_done = asyncio.Queue()
    tasks_running = set()
    # Maximum number of tasks not defined at the start, will be set once a newly spawned task raises an exception
    max_tasks = None

    # Split the period range into smaller ranges according to the workload given to each task
    block_pool = {(k, k + workload - 1) for k in range(period_start, period_end, workload)}
    raw_data = []

    # Track the tasks' runtime history for auto-adjusting the task spawning frequency (if enabled)
    tasks_runtime_history = []
    task_start_time = None

    logging.info('Streaming %i blocks on %s chain...',
        period_end - period_start,
        chain.upper(),
    )

    async with get_secure_channel(chain) as secure_channel:
        spawner_task = asyncio.create_task(_spawner())
        # Wait for spawner to start initial tasks
        await asyncio.sleep(spawn_frequency * initial_tasks)

        while tasks_running:
            # Queue is filled by the workers when exiting (using __task_done_callback)
            task = await tasks_done.get()
            task_exception = task.exception()

            if task_exception is None: # TODO: Check the exception for 'Stream removed' (or other indicating channel failure)
                if auto_adjust_frequency:
                    if not task_start_time:
                        task_start_time = time.perf_counter()
                    else:
                        tasks_runtime_history.append((time.perf_counter() - task_start_time)*0.8)
                        spawn_frequency = statistics.mean(tasks_runtime_history)
                        task_start_time = None

                raw_data += task.result()
            elif not spawner_task.done():
                if not max_tasks or len(tasks_running) < max_tasks:
                    logging.warning('[%s] Maximum number of tasks reached: %i tasks before exception %s',
                        get_current_task_name(),
                        len(tasks_running),
                        '' if not max_tasks else '(updated)'
                    )
                    max_tasks = len(tasks_running)

                if isinstance(task_exception, BlockStreamException): # TODO: More robust if another exception is thrown
                    # Add non-extracted blocks back to the block pool
                    block_pool.add((task_exception.failed, task_exception.end))

    logging.info('Finished block streaming, got %i blocks [SUCCESS]',
        len(raw_data),
    )
    return raw_data

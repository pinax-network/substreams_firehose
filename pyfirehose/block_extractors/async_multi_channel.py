"""
SPDX-License-Identifier: MIT

This extractor is very similar to the `async_single_channel` except that once the first channel has been maxed out of
workers, it tries to open a second gRPC channel to allow for even more workers to be spawned in the new channel.
The block pool is thus shared between all the 'spawner' tasks and dynamically adjusted on creation or destruction of
channels.

This concept, while theoretically possible, isn't fully supported right now by the Python gRPC implementation and/or
by the servers and new channels fails to create any new workers. Prefer to use `async_single_channel` or
`async_optimized` for block extraction.

Diagram: see ['asynchronous_dream_block_streaming.jpg'](block_extractors_explained/asynchronous_dream_block_streaming.jpg)
"""

import asyncio
from itertools import zip_longest
import logging
import statistics
import time

from google.protobuf.message import Message

from pyfirehose.block_extractors.common import get_secure_channel
from pyfirehose.block_extractors.common import stream_blocks
from pyfirehose.config.parser import Config
from pyfirehose.exceptions import BlockStreamException
from pyfirehose.utils import get_current_task_name

TRIGGER_CHANNEL_CREATION_LOCK = asyncio.Lock()

async def asyncio_main(period_start: int, period_end: int, #pylint: disable=too-many-arguments, too-many-locals, too-many-statements
              initial_tasks: int = 25, workload: int = 100, auto_adjust_frequency: bool = False,
              spawn_frequency: float = 0.1, **kwargs) -> list[Message]:
    """
    Extract blocks from a gRPC channel as raw blocks for later processing.

    Using asynchronous directives, a number of workers will be periodically spawned to
    extract data from *multiple* gRPC channels until all blocks have been retrieved.
    The returned list can then be parsed for extracting relevant data from the blocks.

    Args:
        period_start: The first block number of the targeted period.
        period_end: The last block number of the targeted period.
        initial_tasks: The initial number of concurrent tasks to start for streaming blocks.
        workload: The number of blocks to extract for each task.
        auto_adjust_frequency: Enable the task spawner to auto adjust the task spawning frequency based on the tasks' average
        runtime.
        spawn_frequency: The sleep time (in seconds) for the spawner to wait before trying to spawn a new task.
        Will be overridden if `auto_adjust_frequency` is enabled.
        kwargs: Additional keyword arguments to pass to the gRPC request (must match .proto file definition).

    Returns:
        A list of raw blocks (google.protobuf.any_pb2.Any objects) that can later be processed.
    """
    async def _spawner(token):
        data = []
        async with get_secure_channel() as secure_channel:
            async def _task_spawner():
                while True:
                    logging.debug('[%s] %i tasks running | polling every %fs | %i blocks remaining in block_pool["%s"]',
                        get_current_task_name(),
                        len(running),
                        spawn_frequency,
                        len(block_pool[token])*workload,
                        token
                    )

                    try:
                        await asyncio.sleep(spawn_frequency)
                    except asyncio.CancelledError:
                        logging.warning('[%s] Stopping spawner task NOW...', get_current_task_name())
                        return

                    if (max_tasks and len(running) >= max_tasks) or not token in block_pool:
                        continue

                    if not block_pool[token]:
                        logging.warning('[%s] No more blocks in block_pool["%s"], stopping spawner task NOW...',
                            get_current_task_name(),
                            token
                        )
                        return

                    new_task = asyncio.create_task(
                        stream_blocks(
                            *block_pool[token].pop(),
                            secure_channel,
                            **kwargs
                        )
                    )
                    new_task.add_done_callback(_task_done_callback)
                    running.add(new_task)

            def _task_done_callback(task):
                if task.exception():
                    logging.error('%s encountered an exception', task.get_name())
                else:
                    logging.debug('%s finished block streaming', task.get_name())
                running.remove(task)
                done.put_nowait(task)

            logging.info('Streaming %i blocks on %s chain...',
                period_end - period_start + 1,
                Config.CHAIN,
            )

            done = asyncio.Queue()
            running = set()
            max_tasks = None
            tasks_runtime = []
            task_start_time = None
            nonlocal spawn_frequency

            spawner_task = asyncio.create_task(_task_spawner())
            await asyncio.sleep(spawn_frequency*initial_tasks) # Wait for spawner to start initial tasks

            while running:
                task = await done.get()
                task_exception = task.exception()

                if task_exception is None:
                    if auto_adjust_frequency:
                        if not task_start_time:
                            task_start_time = time.perf_counter()
                        else:
                            tasks_runtime.append((time.perf_counter() - task_start_time)*0.8)
                            spawn_frequency = statistics.mean(tasks_runtime)
                            task_start_time = None

                    data += task.result()
                elif not spawner_task.done():
                    if not max_tasks or len(running) < max_tasks:
                        logging.warning('[%s] Maximum number of tasks reached: %i tasks before exception %s',
                            get_current_task_name(),
                            len(running),
                            '' if not max_tasks else '(updated)'
                        )
                        max_tasks = len(running)

                        async with TRIGGER_CHANNEL_CREATION_LOCK: # TODO: Replace with events + prevent triggering if no worker can spawn
                            nonlocal trigger_channel_creation
                            trigger_channel_creation = True

                    if isinstance(task_exception, BlockStreamException): # TODO: More robust if another exception is thrown
                        # Add non-processed blocks back to local_block_pool
                        block_pool[token].add((task_exception.failed, task_exception.end))

        logging.info('[%s] Block streaming done !', get_current_task_name())
        return data

    def reshape_block_pool(split): # TODO: Reshape according to number of workers by spawner (+ runtime)
        unified_block_pool = set.union(*block_pool.values())

        new_block_pool = {}
        key = 0
        for subset in zip_longest(*[iter(unified_block_pool)]*(len(unified_block_pool)//split)):
            new_block_pool[str(key)] = set(filter(None, subset))
            key += 1

        logging.debug('Block pool split: %s', new_block_pool)
        return new_block_pool

    def add_task():
        task = asyncio.create_task(_spawner(str(token)))
        task.add_done_callback(lambda task_done: spawners.remove(task_done))
        spawners.add(task)

    block_diff = period_end - period_start
    # Run only one task if number of block to stream is very small
    if block_diff < initial_tasks:
        initial_tasks = 1
        workload = block_diff
    # Adjust workload to give work to all the tasks in case the number of blocks to stream is too small
    elif block_diff < initial_tasks * workload:
        workload = block_diff//initial_tasks

    trigger_channel_creation = False
    token = 0

    block_pool = {}
    block_pool[str(token)] = {(i, i + workload - 1) for i in range(period_start, period_end, workload)}

    spawners = set()
    add_task()

    pending = True
    previous_pending = 1
    while pending:
        done, pending = await asyncio.wait(spawners, timeout=1)

        if trigger_channel_creation and token == 0:
            token += 1
            add_task()

        if spawners and previous_pending != len(spawners):
            block_pool = reshape_block_pool(len(spawners))
            previous_pending = len(spawners)

    return [item for l in [spawner.result() for spawner in done] for item in l]

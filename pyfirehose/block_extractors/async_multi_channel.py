"""
SPDX-License-Identifier: MIT
"""

import asyncio
from itertools import zip_longest
import logging
import statistics
import time
from typing import List

from google.protobuf.message import Message

from block_extractors.common import get_secure_channel
from block_extractors.common import stream_blocks
from exceptions import BlockStreamException
from utils import get_current_task_name

TRIGGER_CHANNEL_CREATION_LOCK = asyncio.Lock()

async def asyncio_main(period_start: int, period_end: int, chain: str = 'eos', #pylint: disable=too-many-arguments, too-many-locals, too-many-statements
              initial_tasks: int = 25, workload: int = 100, auto_adjust_frequency: bool = False, spawn_frequency: float = 0.1,
              custom_include_expr: str = '', custom_exclude_expr: str = '') -> List[Message]:
    async def _spawner(token):
        data = []
        async with get_secure_channel(chain) as secure_channel:
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
                            custom_include_expr,
                            custom_exclude_expr
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
                period_end - period_start,
                chain.upper(),
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

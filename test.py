#!/usr/bin/env python3

"""
SPDX-License-Identifier: MIT
"""

import asyncio
from itertools import zip_longest
import logging
import statistics
import time

import grpc
from dotenv import load_dotenv
from dotenv import find_dotenv

from exceptions import BlockStreamException
from proto import bstream_pb2
from proto import bstream_pb2_grpc
from utils import get_auth_token
from utils import get_current_task_name

CONSOLE_HANDLER = logging.StreamHandler()
TRIGGER_CHANNEL_CREATION_LOCK = asyncio.Lock()
load_dotenv(find_dotenv())

async def stream_blocks(start, end, secure_channel):
    current_block_number = start
    stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)

    logging.debug('[%s] Starting streaming blocks from #%i to #%i...',
        get_current_task_name(),
        start,
        end
    )

    data = []
    try: # TODO: Investigate why filter expressions makes blocking behavior -> stops parallel execution
        async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
            start_block_num=start,
            stop_block_num=end,
            fork_steps=['STEP_IRREVERSIBLE'],
            include_filter_expr='receiver in ["eosio.bpay", "eosio.vpay"] && action == "transfer"',
        )):
            # block = codec_pb2.Block()
            # # Deserialize google.protobuf.Any to codec.Block
            # response.block.Unpack(block) # TODO: Investigate separating unpacking process after fetching all raw blocks
            # current_block_number = block.number

            # logging.debug('[%s] Parsing block number #%i (%i blocks remaining)...',
            # 	get_current_task_name(),
            # 	current_block_number,
            # 	end - current_block_number
            # )

            # data.append(current_block_number)
            data.append(response.block)
    except grpc.aio.AioRpcError as error: # TODO: More robust if another exception is thrown
        logging.error('[%s] Failed to process block number #%i: %s',
            get_current_task_name(),
            current_block_number,
            error
        )

        raise BlockStreamException(start, end, current_block_number) from error

    logging.debug('[%s] Done !', get_current_task_name())
    return data

async def asyncio_ref(period_start, period_end, max_tasks = 10):
    logging.info('Running %s...', asyncio_ref.__name__)

    jwt = get_auth_token()
    if not jwt:
        return None

    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(jwt)
    )

    block_diff = period_end - period_start + 1
    # Prevent having more tasks than the amount of blocks to process
    split = block_diff//max_tasks

    logging.info('Streaming %i blocks (running %i concurrent tasks)...',
        block_diff,
        max_tasks
    )

    tasks = set()
    data = []
    async with grpc.aio.secure_channel('eos.firehose.eosnation.io:9000', creds) as secure_channel:
        for i in range(max_tasks):
            tasks.add(
                asyncio.create_task(
                    stream_blocks(
                        period_start + i*split,
                        # Gives the remaining blocks to the last task in case the work can't be splitted equally
                        period_start + (i+1)*split - 1 if i < max_tasks-1 else period_end,
                        secure_channel
                    )
                )
            )

        for task in tasks:
            data += await task

    logging.info('Block processing done !')
    return data

async def asyncio_spawner(period_start, period_end, initial_tasks = 10, workload = 100, auto_adjust_frequency = True,
                          spawn_frequency = 0.1):
    async def _spawner(token):
        jwt = get_auth_token()
        if not jwt:
            return None

        creds = grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.access_token_call_credentials(jwt)
        )

        data = []
        async with grpc.aio.secure_channel(
            'eos.firehose.eosnation.io:9000',
            creds,
            options=( # See https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h#L141
                ('grpc.max_concurrent_streams', 30),
            )
        ) as secure_channel:
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

                    new_task = asyncio.create_task(stream_blocks(*block_pool[token].pop(), secure_channel))
                    new_task.add_done_callback(_task_done_callback)
                    running.add(new_task)

            def _task_done_callback(task):
                if task.exception():
                    logging.error('%s encountered an exception', task.get_name())
                else:
                    logging.debug('%s finished block streaming', task.get_name())
                running.remove(task)
                done.put_nowait(task)

            logging.info('[%s] Running %s...', get_current_task_name(), asyncio_spawner.__name__)

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

                        async with TRIGGER_CHANNEL_CREATION_LOCK: # TODO: Replace with events
                            nonlocal trigger_channel_creation
                            trigger_channel_creation = True

                    if isinstance(task_exception, BlockStreamException): # TODO: More robust if another exception is thrown
                        # Add non-processed blocks back to local_block_pool
                        block_pool[token].add((task_exception.failed, task_exception.end))

        logging.info('[%s] Block processing done !', get_current_task_name())
        return data

    def reshape_block_pool(split):
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

def run_test_profiler(period_start, period_end):
    logging_handlers = []

    log_filename = 'logs/test.log'
    logging_handlers.append(logging.FileHandler(log_filename, mode='w+'))

    CONSOLE_HANDLER.setLevel(logging.INFO)
    logging_handlers.append(CONSOLE_HANDLER)

    logging.basicConfig(
        handlers=logging_handlers,
        level=logging.DEBUG,
        format='T+%(relativeCreated)d\t%(levelname)s %(message)s',
        force=True
    )

    logging.addLevelName(logging.DEBUG, '[DEBUG]')
    logging.addLevelName(logging.INFO, '[*]')
    logging.addLevelName(logging.WARNING, '[!]')
    logging.addLevelName(logging.ERROR, '[ERROR]')
    logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

    results = []

    start = time.perf_counter()
    results.append(asyncio.run(asyncio_ref(period_start, period_end, max_tasks=25)))
    logging.info('Time elapsed: %i', time.perf_counter() - start)

    start = time.perf_counter()
    results.append(asyncio.run(asyncio_spawner(period_start, period_end, workload=100, auto_adjust_frequency=True)))
    logging.info('Time elapsed: %i', time.perf_counter() - start)

    # logging.debug('Results: %s', results)
    # logging.info('Same results ? %s', results.count(results[0]) == len(results))
    # logging.info('Diff: %s', list(set(results[0]) ^ set(results[1])))

if __name__ == '__main__':
    START = 272368521
    NB_BLOCKS = 4000
    run_test_profiler(START, START + NB_BLOCKS - 1)

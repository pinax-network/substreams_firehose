#!/usr/bin/env python3

"""
SPDX-License-Identifier: MIT
"""

import asyncio
import importlib
import inspect
import json
import logging
import os
import os.path
import statistics
import time
from datetime import datetime
from typing import Callable, Dict, List, Sequence

import grpc
from dotenv import load_dotenv
from dotenv import find_dotenv
from google.protobuf.message import Message

from args import parse_arguments
from exceptions import BlockStreamException
from proto import bstream_pb2
from proto import bstream_pb2_grpc
from proto import codec_pb2
from utils import date_to_block_num
from utils import get_auth_token
from utils import get_current_task_name

load_dotenv(find_dotenv())

CONSOLE_HANDLER = logging.StreamHandler()
JWT = get_auth_token()

'''
    TODO
    ====

    - Restructure project with separate "block_streamers" according to each architecture
        - Have a top module main to select which streamer to use
        - Have another file for measuring performance of each streamer
    - Add more examples to README.md
    - Drop the generator requirement for block processors (?)
    - Investigate functools and other more abstract modules for block processor modularity (?)
        - Possibility of 3 stages:
            - Pre-processing (e.g. load some API data)
            - Process (currently implemented)
            - Post-processing (e.g. adding more data to transactions)
'''

async def asyncio_main(period_start: int, period_end: int, chain: str = 'eos', #pylint: disable=too-many-arguments, too-many-locals, too-many-statements
              initial_tasks: int = 25, workload: int = 100, auto_adjust_frequency: bool = False, spawn_frequency: float = 0.1,
              custom_include_expr: str = '', custom_exclude_expr: str = '') -> List[Message]:
    """
    Extract blocks from a Firehose endpoint as raw blocks for later processing.

    Using asynchronous directives, a number of workers will be periodically spawned to
    extract data from the gRPC channel until all blocks have been retrieved. The returned
    list can then be parsed for extracting relevant data from the blocks.

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
    async def _stream_blocks(start: int, end: int) -> List[Message]:
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
            async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
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
            logging.info('[%s] %i tasks running | polling every %fs | %i blocks remaining in block pool',
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

            new_task = asyncio.create_task(_stream_blocks(*block_pool.pop()))
            new_task.add_done_callback(__task_done_callback)
            tasks_running.add(new_task)

    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(JWT)
    )

    tasks_done = asyncio.Queue()
    tasks_running = set()
    # Maximum number of tasks not defined at the start, will be set once a newly spawned task raises an exception
    max_tasks = None

    # Split the period range into smaller ranges according to the workload given to each task
    block_pool = {(k, k + workload - 1) for k in range(period_start, period_end, workload)} # TODO: Handle edge case of too many initial_tasks for the job
    raw_data = []

    # Track the tasks' runtime history for auto-adjusting the task spawning frequency (if enabled)
    tasks_runtime_history = []
    task_start_time = None

    logging.info('Streaming %i blocks on %s chain...',
        period_end - period_start,
        chain.upper(),
    )

    async with grpc.aio.secure_channel(
        f'{chain}.firehose.eosnation.io:9000',
        creds,
        # See https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h#L141 for a list of options
        options=(
            ('grpc.max_receive_message_length', os.environ.get('MAX_RECV_BLOCK_SIZE')), # default is 10MB
        )
    ) as secure_channel:
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

def main() -> int:
    """
    Main function for parsing arguments, setting up logging and running asyncio `run` function.
    """
    if not JWT:
        return 1

    logging_handlers = []
    args = parse_arguments()

    # === Arguments checking ===

    if args.end < args.start:
        logging.error('Period start must be less than or equal to period end')
        return 1

    out_file = f'jsonl/{args.chain}_{args.start}_to_{args.end}.jsonl'
    if args.out_file != 'jsonl/{chain}_{start}_to_{end}.jsonl':
        out_file = args.out_file

    log_filename = 'logs/' + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    if args.log != 'logs/{datetime}.log':
        if args.log:
            log_filename = args.log
        logging_handlers.append(logging.FileHandler(log_filename, mode='a+'))

    CONSOLE_HANDLER.setLevel(logging.INFO)
    if args.quiet:
        CONSOLE_HANDLER.setLevel(logging.ERROR) # Keep only errors and critical messages

    module, function = ('block_processors.default', f'{args.chain}_block_processor')
    if args.custom_processor:
        module, function = args.custom_processor.rsplit('.', 1)
        module = f'block_processors.{module}'

    # === Logging setup ===

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

    logging.debug('Script arguments: %s', args)

    # === Block processor loading and startup ===

    try:
        block_processor = getattr(importlib.import_module(module), function)

        if not args.disable_signature_check:
            signature = inspect.signature(block_processor)
            parameters_annotations = [p_type.annotation for (_, p_type) in signature.parameters.items()]

            if (signature.return_annotation == signature.empty
                # If there are parameters and none are annotated
                or (not parameters_annotations and signature.parameters)
                # If some parameters are not annotated
                or any((t == inspect.Parameter.empty for t in parameters_annotations))
            ):
                logging.warning('Could not check block processing function signature '
                                '(make sure parameters and return value have type hinting annotations)')
            elif (not codec_pb2.Block in parameters_annotations
                  or signature.return_annotation != Dict
                  or not inspect.isgeneratorfunction(block_processor)
            ):
                raise TypeError(f'Incompatible block processing function signature:'
                                f' {signature} should be <generator>(block: codec_pb2.Block) -> Dict')
    except (AttributeError, TypeError) as exception:
        logging.critical('Could not load block processing function: %s', exception)
        raise
    else:
        return process_blocks(
            asyncio.run(
                asyncio_main(
                    period_start=args.start,
                    period_end=args.end,
                    chain=args.chain,
                    custom_include_expr=args.custom_include_expr,
                    custom_exclude_expr=args.custom_exclude_expr,
                )
            ),
            block_processor=block_processor,
            out_file=out_file,
        )

if __name__ == '__main__':
    main()

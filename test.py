#!/usr/bin/env python3

"""
SPDX-License-Identifier: MIT
"""

import asyncio
import logging
from typing import Callable, Dict, List, Union

import grpc
from dotenv import load_dotenv
from dotenv import find_dotenv

from exceptions import BlockStreamException
from proto import bstream_pb2
from proto import bstream_pb2_grpc
from proto import codec_pb2
from utils import get_auth_token
from utils import get_current_task_name

CONSOLE_HANDLER = logging.StreamHandler()
load_dotenv(find_dotenv())

async def asyncio_main(initial_tasks = 10, step = 1000, timeout = 0.5):
    async def _stream_blocks(start, end):
        current_block_number = start
        stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)

        logging.debug('[%s] Starting streaming blocks from #%i to #%i...',
            get_current_task_name(),
            start,
            end
        )

        try:
            async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
                start_block_num=start,
                stop_block_num=end,
                fork_steps=['STEP_IRREVERSIBLE'],
            )):
                block = codec_pb2.Block()
                # Deserialize google.protobuf.Any to codec.Block
                response.block.Unpack(block)
                current_block_number = block.number

                logging.debug('[%s] Parsing block number #%i (%i blocks remaining)...',
                    get_current_task_name(),
                    current_block_number,
                    end - current_block_number
                )

                await asyncio.sleep(0)
        except grpc.aio.AioRpcError as error:
            logging.error('[%s] Failed to process block number #%i: %s',
                get_current_task_name(),
                current_block_number,
                error
            )

            raise BlockStreamException(start, end, current_block_number) from error

        return [{'start': start, 'end': end}]

    async def _spawner(block_range_cursor):
        while True:
            try:
                await asyncio.sleep(timeout)
            except asyncio.CancelledError:
                logging.warning('Stopping task spawner NOW...')
                return

            new_task = asyncio.create_task(_stream_blocks(block_range_cursor, block_range_cursor + step))
            new_task.add_done_callback(when_done)
            running.add(new_task)
            block_range_cursor += step + 1
            logging.info('Added new task: %i running', len(running))

    jwt = get_auth_token()
    if not jwt:
        return 1

    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(jwt)
    )

    done = asyncio.Queue()
    running = set()
    def when_done(task):
        running.remove(task)
        done.put_nowait(task)

    block_range_cursor = 1
    for _ in range(initial_tasks):
        task = asyncio.create_task(_stream_blocks(block_range_cursor, block_range_cursor + step))
        task.add_done_callback(when_done)
        running.add(task)
        block_range_cursor += step + 1

    data = []
    spawner_task = asyncio.create_task(_spawner(block_range_cursor))
    async with grpc.aio.secure_channel('eos.firehose.eosnation.io:9000', creds) as secure_channel:
        while running:
            task = await done.get()
            if task.exception() is None:
                data += task.result()
            else:
                if not spawner_task.done():
                    logging.warning('Maximum number of tasks reached: %i tasks before exception', len(running))
                    spawner_task.cancel()

    logging.info('Block processing done !')
    logging.info('data=%s', data)
    return 0

def run_test_profiler():
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

    return asyncio.run(asyncio_main(step=100))

if __name__ == '__main__':
    run_test_profiler()

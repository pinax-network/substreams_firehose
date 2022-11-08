"""
SPDX-License-Identifier: MIT
"""

import asyncio
import logging
import os
from typing import List

import grpc
from google.protobuf.message import Message

from block_extractors.common import stream_blocks
from exceptions import BlockStreamException
from utils import get_auth_token

JWT = get_auth_token()

async def asyncio_main(period_start: int, period_end: int, chain: str = 'eos', initial_tasks: int = 25,
                       custom_include_expr: str = '', custom_exclude_expr: str = '') -> List[Message]:
    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(JWT)
    )

    block_diff = period_end - period_start
    # Prevent having more tasks than the amount of blocks to process
    split = block_diff//initial_tasks if block_diff > initial_tasks else block_diff

    logging.info('Streaming %i blocks (running %i concurrent tasks)...',
        block_diff,
        initial_tasks
    )

    tasks = set()
    data = []
    async with grpc.aio.secure_channel(
        f'{chain}.firehose.eosnation.io:9000',
        creds,
        # See https://github.com/grpc/grpc/blob/master/include/grpc/impl/codegen/grpc_types.h#L141 for a list of options
        options=[
            ('grpc.max_receive_message_length', os.environ.get('MAX_BLOCK_SIZE')), # default is 8MB
            ('grpc.max_send_message_length', os.environ.get('MAX_BLOCK_SIZE')), # default is 8MB
        ]
    ) as secure_channel:
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

    logging.info('Block processing done !')
    return data

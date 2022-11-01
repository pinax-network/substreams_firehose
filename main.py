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
from datetime import datetime
from typing import Callable, Dict, List, Union

import grpc
from dotenv import load_dotenv
from dotenv import find_dotenv

from exceptions import BlockStreamException
from proto import bstream_pb2
from proto import bstream_pb2_grpc
from proto import codec_pb2
from utils import date_to_block_num
from utils import get_auth_token
from utils import get_current_task_name
from utils import parse_arguments

CONSOLE_HANDLER = logging.StreamHandler()
load_dotenv(find_dotenv())

'''
    TODO
    ====

    - Error-checking for input arguments
        - Move it to its own file using arparse 'type=' as input validators
    - Add opt-in integrity verification (using codec.Block variables)
    - Add more examples to README.md
    - Drop the generator requirement for block processors (?)
    - Optimize asyncio workers: have separate script for measuring the optimal parameters (?)
        - How many blocks can I get from the gRPC connection at once ? Or is it one-by-one ?
        - Detect when running slow and reset connection (resuming work)
        - Change the model:
            - Pool of blocks available for tasks
            - Startup X workers initially getting block ranges from the pool
            - Try to add more workers periodically
                - If exception from one of the workers, timeout and restart it until threshold
                - If exception from last added worker, stop adding worker to this channel and create new one
                - If channel fails, stop adding more workers
            - Tasks return results and `done_callback` startup new task to continue processing (if needed)
            - Any failed task notify with exception and return non-processed blocks to pool
            - Algorithm determines best pool ranges for performance (?)
    - Investigate functools and other more abstract modules for block processor modularity (?)
        - Possibility of 3 stages:
            - Pre-processing (e.g. load some API data)
            - Process (currently implemented)
            - Post-processing (e.g. adding more data to transactions)
'''

async def asyncio_main(accounts: List[str], period_start: Union[int, datetime], period_end: Union[int, datetime], #pylint: disable=too-many-arguments, too-many-locals, too-many-statements
              block_processor: Callable[[codec_pb2.Block], Dict], out_file: str, chain: str = 'eos',
              max_tasks: int = 20, max_retries = 3, custom_include_expr: str = '', custom_exclude_expr: str = '') -> int:
    """
    Write a `.jsonl` file containing relevant transactions related to a list of accounts for a given period.

    It firsts obtains a JWT token from the `AUTH_ENDPOINT` defined in the `.env` file and uses this token
    to authenticate with the Firehose gRPC service associated with the given chain. Then splits the block
    range into smaller ranges to process blocks in parallel using the `block_processor` function.
    Finally, it compiles all recorded transactions into a single `.jsonl` file in the `jsonl/` folder.

    Args:
        accounts:
            The accounts to look for as either recipient or sender of a transaction.
        period_start:
            The first block number or starting date of the targeted period.
        period_end:
            The last block number or ending date of the targeted period.
        block_processor:
            A generator function extracting relevant properties from a block.
        out_file:
            The path or filename for the output data file.
        chain:
            The target blockchain.
        max_tasks:
            The maximum number of concurrent tasks for streaming blocks.
        max_retries:
            The total maximum number of retries for failed block streaming tasks.
        custom_include_expr:
            A custom Firehose filter for tagging blocks as included.
        custom_exclude_expr:
            A custom Firehose filter for excluding blocks from the results.
    """
    async def _block_streaming_task(start: int, end: int) -> List[Dict]:
        async def _stream_blocks(start: int, end: int) -> List[Dict]:
            """
            Return a subset of transactions for blocks between `start` and `end` filtered by targeted accounts.

            Args:
                start:
                    The Firehose stream's starting block.
                end:
                    The Firehose stream's ending block.

            Returns:
                A list of dictionaries describing the matching transactions. For example:
                [
                    {
                        "account": "eosio.bpay",
                        "date": "2022-10-21 00:03:31",
                        "timestamp": 1666310611,
                        "amount": "344.5222",
                        "token": "EOS",
                        "from": "eosio.bpay",
                        "to": "newdex.bp",
                        "block_num": 274268407,
                        "transaction_id": "353555074901da28cd6dd64b0b64e73f12fdc86a91c8ad5e25b68952979aeed0",
                        "memo": "producer block pay",
                        "contract": "eosio.token",
                        "action": "transfer"
                    },
                    ...
                ]
            """
            transactions = []
            current_block_number = start
            stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)

            logging.debug('[%s] Starting streaming blocks from #%i to #%i using "%s"...',
                get_current_task_name(),
                start,
                end,
                block_processor.__name__
            )

            try:
                async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
                    start_block_num=start,
                    stop_block_num=end,
                    fork_steps=['STEP_IRREVERSIBLE'],
                    include_filter_expr=custom_include_expr if custom_include_expr else f'receiver in {accounts} && action == "transfer"',
                    exclude_filter_expr=custom_exclude_expr if custom_exclude_expr else 'action == "*"'
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

                    for transaction in block_processor(block): # TODO: Add exception handling
                        transactions.append(transaction)
            except grpc.aio.AioRpcError as error:
                logging.error('[%s] Failed to process block number #%i: %s',
                    get_current_task_name(),
                    current_block_number,
                    error
                )

                raise BlockStreamException(start, end, current_block_number) from error

            logging.debug('[%s] Done !\n', get_current_task_name())
            return transactions

        tries = 0
        data = []

        while tries < max_retries:
            try:
                data = await _stream_blocks(start, end)
                print(f'[{get_current_task_name()}] data={data}')
            except BlockStreamException as error:
                logging.warning(error)
                start = error.failed
                tries += 1
            else:
                break

        if tries == max_retries:
            raise RuntimeError(f'Max retries reached for {get_current_task_name()} ({max_retries}/{max_retries})')

        return data

    jwt = get_auth_token()
    if not jwt:
        return 1

    if isinstance(period_start, datetime):
        period_start = date_to_block_num(period_start, jwt)
    if isinstance(period_end, datetime):
        period_end = date_to_block_num(period_end, jwt)

    if not (period_start and period_end):
        logging.error('Invalid period: start=%i, end=%i', period_start, period_end)
        return 1
    if period_end < period_start:
        logging.error('period_start must be less than or equal to period_end')
        return 1

    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(jwt)
    )

    block_diff = period_end - period_start
    # Prevent having more tasks than the amount of blocks to process
    max_tasks = block_diff if block_diff < max_tasks else max_tasks
    split = block_diff//max_tasks

    tasks = []
    for i in range(max_tasks):
        tasks.append(
            asyncio.create_task(
                _block_streaming_task(
                    period_start + i*split,
                    # Gives the remaining blocks to the last task in case the work can't be splitted equally
                    period_start + (i+1)*split - 1 if i < max_tasks-1 else period_end,
                )
            )
        )

    logging.info('Streaming %i blocks on %s chain for data related to %s (running %i concurrent tasks)...',
        block_diff,
        chain.upper(),
        accounts,
        max_tasks
    )
    CONSOLE_HANDLER.terminator = '\r'

    # TODO: Test exceptions, optimize
    data = []
    secure_channel = grpc.aio.secure_channel(f'{chain}.firehose.eosnation.io:9000', creds)
    async with secure_channel:
        for task in asyncio.as_completed(tasks):
            try:
                data += await task
            except RuntimeError as error:
                logging.error('[%s] %s', task, error)
                secure_channel = grpc.aio.secure_channel(f'{chain}.firehose.eosnation.io:9000', creds)

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w', encoding='utf8') as out:
        for entry in data:
            json.dump(entry, out) # TODO: Add exception handling
            out.write('\n')

    CONSOLE_HANDLER.terminator = '\n'
    logging.info('\nFinished block streaming, wrote %i rows of data to %s [SUCCESS]',
        len(data),
        out_file
    )

    return 0

def main() -> int:
    """
    Main function for parsing arguments, setting up logging and running asyncio `run` function.
    """
    logging_handlers = []
    args = parse_arguments()

    # === Arguments checking ===

    try:
        args.start = int(args.start)
    except ValueError:
        args.start = datetime.fromisoformat(args.start)

    try:
        args.end = int(args.end)
    except ValueError:
        args.end = datetime.fromisoformat(args.end)

    out_file = f'jsonl/{args.chain}_{"_".join(args.accounts)}_{args.start}_to_{args.end}.jsonl'
    if args.out_file != 'jsonl/{chain}_{accounts}_{start}_to_{end}.jsonl':
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
                logging.warning('Could not check block processing function signature'
                                '(make sure parameters and return value have type hinting annotations)')
            elif (not codec_pb2.Block in parameters_annotations
                  or signature.return_annotation != Dict
                  or not inspect.isgeneratorfunction(block_processor)
            ):
                raise TypeError(f'Incompatible block processing function signature:'
                                f' {signature} should be <generator>(block: codec_pb2.Block) -> Dict')
    except (AttributeError, TypeError) as exception: # TODO: Use exception group
        logging.critical('Could not load block processing function: %s', exception)
        return 1
    else:
        return asyncio.run(
            asyncio_main(
                accounts=args.accounts,
                period_start=args.start,
                period_end=args.end,
                block_processor=block_processor,
                out_file=out_file,
                chain=args.chain,
                max_tasks=args.max_tasks,
                custom_include_expr=args.custom_include_expr,
                custom_exclude_expr=args.custom_exclude_expr,
            )
        )

if __name__ == '__main__':
    main()

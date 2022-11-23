#!/usr/bin/env python3

"""
SPDX-License-Identifier: MIT

Main entry point of the application.
"""

import asyncio
import importlib
import inspect
import json
import logging
import os
from argparse import ArgumentTypeError
from datetime import datetime

from hjson import HjsonDecodeError

#pylint: disable=wrong-import-position
from args import check_period, parse_arguments
from block_extractors.common import process_blocks
from config import Config
from config import load_config
from proto.generated.dfuse.eosio.codec.v1 import codec_pb2
from utils import get_auth_token
#pylint: enable=wrong-import-position

CONSOLE_HANDLER = logging.StreamHandler()

def main() -> int: #pylint: disable=too-many-statements, too-many-branches
    """
    Main function for parsing arguments, setting up logging and running asyncio `run` function.
    """
    logging_handlers = []
    args = parse_arguments()

    # === Arguments checking ===

    try:
        load_config(args.config)
    except (HjsonDecodeError, ImportError, KeyError):
        return 1

    try:
        args.start = check_period(args.start)
        args.end = check_period(args.end)
    except ArgumentTypeError:
        return 1

    if args.end < args.start:
        logging.error('Period start must be less than or equal to period end')
        return 1

    out_file = f'jsonl/{Config.CHAIN}_{args.start}_to_{args.end}.jsonl'
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

    try:
        block_extractor = getattr(
            importlib.import_module(
                f'block_extractors.async_{args.extractor + "_channel" if args.extractor != "optimized" else args.extractor}'
            ),
            'asyncio_main'
        )
    except (AttributeError, TypeError) as exception:
        logging.critical('Could not load block extractor function: %s', exception)
        raise

    module, function = ('block_processors.dfuse.default', f'{Config.CHAIN.lower()}_block_processor')
    if args.custom_processor:
        module, function = args.custom_processor.rsplit('.', 1)
        module = f'block_processors.{module}'

    # === Logging setup ===

    logging_handlers.append(CONSOLE_HANDLER)

    logging.basicConfig(
        handlers=logging_handlers,
        level=logging.DEBUG,
        format='%(asctime)s:T+%(relativeCreated)d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True
    )

    logging.addLevelName(logging.DEBUG, '[DEBUG]')
    logging.addLevelName(logging.INFO, '[*]')
    logging.addLevelName(logging.WARNING, '[!]')
    logging.addLevelName(logging.ERROR, '[ERROR]')
    logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

    logging.debug('Script arguments: %s', args)

    # === JWT token validation ===

    jwt = get_auth_token()
    if not jwt:
        logging.critical('Could not get authentication token from endpoint (%s), aborting...', Config.AUTH_ENDPOINT)
        return 1

    # === Block processor loading and startup ===

    try:
        block_processor = getattr(importlib.import_module(module), function)

        # if not args.disable_signature_check: # TODO: Rework depending on protobuf (or remove entirely ?)
        # 	signature = inspect.signature(block_processor)
        # 	parameters_annotations = [p_type.annotation for (_, p_type) in signature.parameters.items()]

        # 	if (signature.return_annotation == signature.empty
        # 		# If there are parameters and none are annotated
        # 		or (not parameters_annotations and signature.parameters)
        # 		# If some parameters are not annotated
        # 		or any((t == inspect.Parameter.empty for t in parameters_annotations))
        # 	):
        # 		logging.warning('Could not check block processing function signature '
        # 						'(make sure parameters and return value have type hinting annotations)')
        # 	elif (not codec_pb2.Block in parameters_annotations
        # 		  or signature.return_annotation != dict
        # 		  or not inspect.isgeneratorfunction(block_processor)
        # 	):
        # 		raise TypeError(f'Incompatible block processing function signature:'
        # 						f' {signature} should be <generator>(block: codec_pb2.Block) -> Dict')
    except (AttributeError, TypeError) as exception:
        logging.critical('Could not load block processing function: %s', exception)
        raise

    # === Main methods calls ===

    data = process_blocks(
        asyncio.run(
            block_extractor(
                period_start=args.start,
                period_end=args.end,
            )
        ),
        block_processor=block_processor
    )

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w', encoding='utf8') as out:
        for entry in data:
            json.dump(entry, out) # TODO: Add exception handling
            out.write('\n')

    logging.info('Wrote %i rows of data to %s [SUCCESS]', len(data), out_file)
    return 0

if __name__ == '__main__':
    main()

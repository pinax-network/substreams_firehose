#!/usr/bin/env python3

"""
SPDX-License-Identifier: MIT

Main entry point of the application.
"""

import asyncio
import importlib
import json
import logging
import os
from argparse import ArgumentError, ArgumentTypeError
from datetime import datetime
from pprint import pformat

from hjson import HjsonDecodeError

from pyfirehose.args import check_period, parse_arguments
from pyfirehose.block_extractors.common import process_blocks
from pyfirehose.config.parser import Config, StubConfig
from pyfirehose.config.parser import load_config, load_stub_config
from pyfirehose.utils import get_auth_token

CONSOLE_HANDLER = logging.StreamHandler()

def main() -> int: #pylint: disable=too-many-statements, too-many-branches, too-many-locals
    """
    Main function for parsing arguments, setting up logging and running asyncio main loop.
    """
    logging_handlers = []
    args = parse_arguments()

    # === Logging setup ===

    log_filename = 'logs/' + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    if args.log != 'logs/{datetime}.log':
        if args.log:
            log_filename = args.log
        logging_handlers.append(logging.FileHandler(log_filename, mode='a+' if not args.overwrite_log else 'w'))

    CONSOLE_HANDLER.setLevel(logging.INFO)
    if args.quiet:
        # Keep only errors and critical messages
        CONSOLE_HANDLER.setLevel(logging.ERROR)

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

    # === Config loading ===

    try:
        stub_loaded = load_config(args.config, args.grpc_entry)
    except (HjsonDecodeError, ArgumentTypeError, ImportError, KeyError) as error:
        logging.critical('Error loading config file: %s', error)
        raise

    if args.stub:
        try:
            load_stub_config(args.stub)
        except (HjsonDecodeError, ImportError, KeyError) as error:
            logging.critical('Error loading stub config file: %s', error)
            raise
    elif not stub_loaded:
        logging.critical('Stub config should be supplied either in the main config file or through the CLI option.')
        raise ArgumentError

    logging.debug('Main config: %s', pformat(vars(Config)))
    logging.debug('Stub config: %s', pformat(vars(StubConfig)))

    # === JWT token validation ===

    jwt = get_auth_token()
    if not jwt:
        logging.critical('Could not get authentication token from endpoint (%s), aborting...', Config.AUTH_ENDPOINT)
        raise RuntimeError

    # === Arguments checking ===

    args.start = check_period(args.start)
    args.end = check_period(args.end)

    if args.end < args.start:
        logging.critical('Period start must be less than or equal to period end')
        raise ArgumentError

    out_file = f'jsonl/{Config.CHAIN}_{args.start}_to_{args.end}.jsonl'
    if args.out_file != 'jsonl/{chain}_{start}_to_{end}.jsonl':
        out_file = args.out_file

    try:
        block_extractor = getattr(
            importlib.import_module(
                f'pyfirehose.block_extractors.async_{args.extractor + ("_channel" if args.extractor != "optimized" else "")}'
            ),
            'asyncio_main'
        )
    except (AttributeError, TypeError) as exception:
        logging.critical('Could not load block extractor function: %s', exception)
        raise

    module, function = ('pyfirehose.block_processors.processors', args.custom_processor)

    try:
        block_processor = getattr(importlib.import_module(module), function)
    except (AttributeError, TypeError) as exception:
        logging.critical('Could not load block processing function: %s', exception)
        raise

    request_parameters_args = {}
    if args.request_parameters:
        for key, value in [x.split('=', 1) for x in args.request_parameters]:
            if key in ['start_block_num', 'stop_block_num']:
                raise ArgumentTypeError('Cannot use "start_block_num" or "stop_block_num" as additional keyword arguments')
            request_parameters_args[key] = int(value) if value.isdigit() else value

    args.request_parameters = request_parameters_args

    # === Main methods calls ===

    data = process_blocks(
        asyncio.run(
            block_extractor(
                period_start=args.start,
                period_end=args.end,
                **args.request_parameters
            )
        ),
        block_processor=block_processor
    )

    # === Output data to file ===

    try:
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, 'w', encoding='utf8') as out:
            for entry in data:
                if args.no_json_output:
                    out.write(entry)
                else:
                    json.dump(entry, out) # TODO: Add exception handling
                out.write('\n')
    except OSError as error:
        logging.error('Could not write out file to "%s": %s', out_file, error)

    logging.info('Wrote %i rows of data to %s [SUCCESS]', len(data), out_file)
    return 0

if __name__ == '__main__':
    main()

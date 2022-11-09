#!/usr/bin/env python3

"""
SPDX-License-Identifier: MIT

This script compares the throughput performance of multiple block extractors.
"""

import asyncio
import logging
import random
import time

from dotenv import load_dotenv
from dotenv import find_dotenv

# Load .env before local imports for enabling authentication token queries
load_dotenv(find_dotenv())

#pylint: disable=wrong-import-position
# from block_extractors.async_multi_channel import asyncio_main as async_multi
from block_extractors.async_single_channel import asyncio_main as async_single
from block_extractors.async_optimized import asyncio_main as async_optimized
#pylint: enable=wrong-import-position

CONSOLE_HANDLER = logging.StreamHandler()

def main() -> int:
    logging_handlers = []
    logging_handlers.append(CONSOLE_HANDLER)

    logging.basicConfig(
        handlers=logging_handlers,
        level=logging.CRITICAL,
        format='T+%(relativeCreated)d\t%(levelname)s %(message)s',
        force=True
    )

    logging.addLevelName(logging.DEBUG, '[DEBUG]')
    logging.addLevelName(logging.INFO, '[*]')
    logging.addLevelName(logging.WARNING, '[!]')
    logging.addLevelName(logging.ERROR, '[ERROR]')
    logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

    logger = logging.getLogger('perf')
    logging.getLogger('perf').setLevel(logging.INFO)

    accounts = ['eosio.bpay', 'eosio.bpay']
    n_blocks = 100_000
    logger.info('Comparing performance for extracting %i blocks targeting %s transfers on EOS blockchain',
        n_blocks,
        accounts,
    )

    throughput = {}

    for extractor in (async_optimized, async_single):
        period_start = random.randint(217_418_470, 267_418_470)
        logger.info('[%s] Starting streaming at height %i...', extractor.__module__, period_start)
        time_start = time.perf_counter()
        asyncio.run(
            extractor(
                period_start,
                period_start + n_blocks,
                custom_include_expr=f'receiver in {accounts} && action == "transfer"',
            )
        )

        elapsed = time.perf_counter() - time_start
        throughput[extractor.__module__] = n_blocks//elapsed
        logger.info('[%s] Extracted %i blocks in %fs (avg. %i blocks/s)',
            extractor.__module__,
            n_blocks,
            elapsed,
            throughput[extractor.__module__]
        )

    logger.info('=== Results ===')
    fastest = max(throughput, key=throughput.get)
    for key, value in throughput.items():
        if key != fastest:
            logger.info('"%s" is faster than "%s" by %.2f%% (+%i blocks/s)',
                fastest,
                key,
                (throughput[fastest]/value - 1)*100,
                throughput[fastest] - value
            )

if __name__ == '__main__':
    main()

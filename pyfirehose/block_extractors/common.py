"""
SPDX-License-Identifier: MIT
"""

import json
import logging
import os
import os.path
from typing import Callable, Dict, Sequence

from google.protobuf.message import Message

from proto import codec_pb2

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

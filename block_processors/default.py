"""
SPDX-License-Identifier: MIT

This module provides the default block processors for the Firehose supported chains (see https://docs.dfuse.eosnation.io/eosio/public-apis/reference/network-endpoints/). # pylint: disable=line-too-long
"""

import json
import logging
from datetime import datetime
from typing import Dict

from proto import codec_pb2
from utils import get_current_task_name

def eos_block_processor(block: codec_pb2.Block) -> Dict:
    """
    Yield a processed transaction from a block returning relevant properties.

    The signature of the function is crucial: it must take a `Block` object
    (properties defined in the `proto/codec.proto` file) and return a dict
    containing the desired properties for later storage in the `.jsonl` file.

    The basic template for processing transactions should look like this:
    ```
        for transaction_trace in block.filtered_transaction_traces: # Gets every filtered TransactionTrace from a Block
            for action_trace in transaction_trace.action_traces: # Gets every ActionTrace within a TransactionTrace
                if not action_trace.filtering_matched: # Only keep 'transfer' actions that matched the filters
                    continue

                data = {}

                # Process the data...

                yield data
    ```
    See `proto/codec.proto` file for a full list of available objects and properties.

    Args:
        block:
            The block to process transaction from.

    Yields:
        A dictionary containing the extracted block data.

        Example:
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
            }
    """
    for transaction_trace in block.filtered_transaction_traces:
        for action_trace in transaction_trace.action_traces:
            if not action_trace.filtering_matched:
                continue

            action = action_trace.action
            try:
                json_data = json.loads(action.json_data)
            except json.JSONDecodeError as error:
                logging.warning('[%s] Could not parse action (trxid=%s): %s\n',
                    get_current_task_name(),
                    action_trace.transaction_id,
                    error
                )
                continue

            amount, token = json_data['quantity'].split(' ')
            data = {
                'account': action_trace.receiver,
                'date': datetime.utcfromtimestamp(action_trace.block_time.seconds).strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': action_trace.block_time.seconds,
                'amount': amount,
                'token': token,
                'from': json_data['from'],
                'to': json_data['to'],
                'block_num': transaction_trace.block_num,
                'transaction_id': action_trace.transaction_id,
                'memo': json_data['memo'],
                'contract': action.account,
                'action': action.name,
            }

            logging.debug('[%s] %s', get_current_task_name(), data)
            yield data

def wax_block_processor(block: codec_pb2.Block) -> Dict:
    """
    Same as eos_block_processor.
    """
    yield from eos_block_processor(block)

def kylin_block_processor(block: codec_pb2.Block) -> Dict:
    """
    Same as eos_block_processor.
    """
    yield from eos_block_processor(block)

def jungle4_block_processor(block: codec_pb2.Block) -> Dict:
    """
    Same as eos_block_processor.
    """
    yield from eos_block_processor(block)

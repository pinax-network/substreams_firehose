"""
SPDX-License-Identifier: MIT

This module provides block processors used to extract information from the blocks extracted from a gRPC stream.
"""

import json
import logging
from datetime import datetime
from typing import Optional

from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message

from pyfirehose.utils import import_all_from_module

def _unpack_block(raw_block: Message, block_type_name: Optional[str] = 'Block') -> Message:
    """
    Unpack a raw block to the appropriate block object determined by the raw block `Any.type_url`.

    It requires the compiled proto to be present in the `proto.generated` submodule
    with the block type named as `Block` by default.

    See the [protobuf `Any` docs](https://googleapis.dev/python/protobuf/latest/google/protobuf/any_pb2.html) for more info.

    Args:
        raw_block: `Any` message type representing a raw block from the gRPC stream.
        block_type_name: Name of the block object in the generated protobuf files ('Block' by default).

    Returns:
        The loaded block object.

    Raises:
        ImportError: If the extracted block type is not present in the generated protobuf files.

    Example:
        A `type_url` equal to `type.googleapis.com/sf.antelope.type.v1.Block` will import and unpack the block from
        the `pyfirehose.proto.generated.sf.antelope.type.v1' module as `Block()`.
    """
    block = None
    block_type = raw_block.type_url.split("/")[1].rsplit(".", 1)[0]
    logging.debug('Block type : %s', block_type)

    imported = import_all_from_module(f'pyfirehose.proto.generated.{block_type}')
    for module in imported:
        try:
            block = getattr(module, block_type_name)()
        except AttributeError:
            pass

    if not block:
        logging.error('Could not determine block type from Message: ' \
            'check that "%s" exists in the "proto.generated" submodule.',
            block_type
        )
        raise ImportError

    raw_block.Unpack(block)
    return block

def default_block_processor(raw_block: Message) -> dict:
    """
    Yield all the block data as a JSON-formatted dictionary.

    First unpacks the block and converts all its properties to JSON.

    Args:
        raw_block: Raw block received from the gRPC stream.

    Yields:
        A dictionary containing all the block's properties as defined in the proto files.
    """
    block = _unpack_block(raw_block)
    data = json.loads(MessageToJson(block))

    logging.debug('Data: %s', data)
    yield data

def filtered_block_processor(raw_block: Message) -> dict:
    """
    Yield a all transactions from a gRPC filtered block, returning a subset of relevant properties.

    See the `README.md` file for more information on building filtered stream.

    Args:
        raw_block: Raw block received from the gRPC stream.

    Yields:
        A dictionary containing the filtered block data.

    Example:
    ```json
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
    ```
    """
    block = _unpack_block(raw_block)
    for transaction_trace in block.filtered_transaction_traces:
        for action_trace in transaction_trace.action_traces:
            if not action_trace.filtering_matched:
                continue

            action = action_trace.action
            try:
                json_data = json.loads(action.json_data)
            except json.JSONDecodeError as error:
                logging.warning('Could not parse action (trxid=%s): %s\n',
                    action_trace.transaction_id,
                    error
                )
                continue

            # TODO: Handle exceptions for missing keys in json_data
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

            logging.debug('Data: %s', data)
            yield data

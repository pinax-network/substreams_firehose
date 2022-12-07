"""
SPDX-License-Identifier: MIT

This module provides default block processors for *Firehose v1* supported chains
(see https://docs.dfuse.eosnation.io/eosio/public-apis/reference/network-endpoints/).
"""

import json
import logging
from datetime import datetime

from google.protobuf.message import Message
from proto.generated.dfuse.eosio.codec.v1 import codec_pb2

def default_block_processor(raw_block: Message) -> dict:
    """
    Yield a processed transaction from a block returning relevant properties.

    See `proto/codec.proto` file for a full list of available properties.

    Args:
        raw_block:
            Raw block received from the gRPC stream.

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
    block = codec_pb2.Block()
    raw_block.Unpack(block)
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

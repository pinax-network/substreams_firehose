"""
SPDX-License-Identifier: MIT

Provides block processors to parse information from the extracted blocks of a gRPC stream.
"""

import json
import logging
from datetime import datetime
from typing import Iterator

from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message

from substreams_firehose.config.parser import StubConfig
from substreams_firehose.utils import filter_keys

def _filter_data(data: Message, _filter: dict) -> dict:
    """
    Return the output of a gRPC response as JSON data using the stub config's output filter.

    Args:
        data: The output message from a gRPC service.
        _filter: The nested dictionary filter.

    Returns:
        A dictionary representing the filtered output data as JSON.
    """

    json_data = json.loads(MessageToJson(data, preserving_proto_field_name=True))
    return filter_keys(json_data, _filter) if _filter else json_data

def default_processor(data: Message) -> Iterator[dict]:
    """
    Yield the filtered output of a gRPC response.

    Args:
        data: The output message from a gRPC service.

    Yields:
        The filtered data.
    """
    yield _filter_data(data, StubConfig.RESPONSE_PARAMETERS)

def default_substream_processor(data: Message) -> Iterator[dict]:
    """
    Yield filtered output data from a Substreams-enabled gRPC endpoint.

    Args:
        data: The output message from the substream.

    Yields:
        The filtered data according to the output modules present.
    """
    for output in data.outputs:
        yield _filter_data(output.map_output, StubConfig.RESPONSE_PARAMETERS[output.name])

def filtered_block_processor(raw_block: Message) -> Iterator[dict]:
    """
    Yield all transactions from a Firehose V1 gRPC filtered block, returning a subset of relevant properties.

    See the [`README.md`](../../../README.md) file for more information on building filtered stream.

    Args:
        raw_block: A raw block received from the gRPC stream.

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
    data = _filter_data(raw_block, StubConfig.RESPONSE_PARAMETERS)

    try:
        for transaction_trace in data['filtered_transaction_traces']:
            for action_trace in transaction_trace['action_traces']:
                if not 'filtering_matched' in action_trace:
                    continue

                action = action_trace['action']
                try:
                    json_data = json.loads(action['json_data'])
                except json.JSONDecodeError as error:
                    logging.warning('Could not parse action (trxid=%s): %s\n',
                        action_trace['transaction_id'],
                        error
                    )
                    continue

                amount, token = json_data['quantity'].split(' ')
                date = datetime.strptime(action_trace['block_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                data = {
                    'account': action_trace['receiver'],
                    'date': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'timestamp': date.timestamp(),
                    'amount': amount,
                    'token': token,
                    'from': json_data['from'],
                    'to': json_data['to'],
                    'block_num': transaction_trace['block_num'],
                    'transaction_id': action_trace['transaction_id'],
                    'memo': json_data['memo'],
                    'contract': action['account'],
                    'action': action['name'],
                }

                logging.debug('Data: %s', data)
                yield data
    except KeyError as error:
        logging.warning('Skipping block : %s missing from output', error)

"""
SPDX-License-Identifier: MIT

Provides block processors to parse information from the extracted blocks of a gRPC stream.
"""

import json
import logging
from collections.abc import Mapping, Sequence
from datetime import datetime

from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message

from pyfirehose.config.parser import Config, StubConfig

def filtered_block_processor(raw_block: Message) -> dict:
    """
    Yield all transactions from a Firehose V1 gRPC filtered block, returning a subset of relevant properties.

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
    data = _filtered_data(raw_block)

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

                # TODO: Handle exceptions for missing keys in json_data
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

def _filtered_data(data: Message) -> dict:
    """
    Return the output of a gRPC response as JSON data using the stub config's output filter.

    Args:
        data: The output message from a gRPC service.

    Returns:
        A dictionary representing the filtered output data as JSON.
    """
    def __filter_keys(input_: dict, keys_filter: dict) -> dict:
        """
        Recursively filters the `input_` dictionary based on the keys present in `keys_filter`.

        Args:
            input_: The input nested dict to filter.
            keys_filter: The nested dict filter matching subset of keys present in the `input_`.

        Returns:
            The filtered `input_` as a new dict.

        Examples:
        #### Input
        ```json
        {
            'a': 'value',
            'b': {
                'b1': 'important stuff',
                'b2': {
                    'x': 'stop nesting stuff',
                    'y': 'keep me !'
                }
            },
            'c': {
                'c1': [1, 2, 3],
                'c2': 'Hello'
            },
            'd': [
                {'d1': 1},
                {'d1': 2, 'd2': 3}
            ]
        }
        ```
        #### Filter
        ```json
        {
            'a': True,
            'b': {
                'b1': True,
                'b2': {
                    'y': True
                }
            },
            'c': {
                'c1': True
            },
            'd': {
                'd1': True,
            }
        }
        ```
        #### Output
        ```json
        {
            'a': 'value',
            'b': {
                'b1': 'important stuff',
                'b2': {
                    'y': 'keep me !'
                }
            },
            'c': {
                'c1': [1, 2, 3],
            },
            'd': [
                {'d1': 1},
                {'d1': 2}
            ]
        }
        ```
        """
        output = {}
        for key, value in input_.items():
            if keys_filter == "True":
                output[key] = value
            elif key in keys_filter:
                if isinstance(value, Sequence):
                    if value and isinstance(value[0], dict):
                        output[key] = [__filter_keys(element, keys_filter[key]) for element in value]
                    else:
                        output[key] = value
                elif isinstance(value, Mapping):
                    output[key] = __filter_keys(value, keys_filter[key])
                else:
                    output[key] = value

        return output

    json_data = json.loads(MessageToJson(data, preserving_proto_field_name=True))
    return __filter_keys(json_data, StubConfig.RESPONSE_PARAMETERS) if StubConfig.RESPONSE_PARAMETERS else json_data

def default_processor(data: Message) -> dict:
    """
    Yield the filtered output of a gRPC response.

    Args:
        data: The output message from a gRPC service.

    Yields:
        The filtered data.
    """
    yield _filtered_data(data)

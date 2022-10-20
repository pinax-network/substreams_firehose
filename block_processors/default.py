import asyncio
import json
import logging

from datetime import datetime
from proto import codec_pb2
from typing import Dict

def get_current_task_name() -> str:
	"""
	Helper function for generating a unique task id in the log file.
	"""
	return asyncio.current_task().get_name()

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
				if not action_trace.filtering_matched: # Only keep 'transfer' actions that concerns the targeted accounts
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
				"date": "2022-10-10 00:00:12",
				"timestamp": 1665360012,
				"amount": "40.1309",
				"token": "EOS",
				"amountCAD": 0,
				"token/CAD": 0,
				"from": "eosio",
				"to": "eosio.bpay",
				"block_num": 272368521, 
				"transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", 
				"memo": "fund per-block bucket", 
				"contract": "eosio.token", 
				"action": "transfer"
			}
	"""
	logging.debug(f'[{get_current_task_name()}] block={block}')
	for transaction_trace in block.filtered_transaction_traces:
		for action_trace in transaction_trace.action_traces:
			if not action_trace.filtering_matched:
				continue

			action = action_trace.action
			try:
				json_data = json.loads(action.json_data)
			except Exception as e:
				logging.warning(f'[{get_current_task_name()}] Could not parse action (trxid={action_trace.transaction_id}): {e}\n')
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

			logging.debug(f'[{get_current_task_name()}] {data}')
			yield data

def wax_block_processor(block: codec_pb2.Block) -> Dict:
	"""
	Same as eos_block_processor.
	"""
	return eos_block_processor(block)

def kylin_block_processor(block: codec_pb2.Block) -> Dict:
	"""
	Same as eos_block_processor.
	"""
	return eos_block_processor(block)

def jungle4_block_processor(block: codec_pb2.Block) -> Dict:
	"""
	Same as eos_block_processor.
	"""
	return eos_block_processor(block)
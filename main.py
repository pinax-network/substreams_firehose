import argparse
import asyncio
import grpc
import json
import logging
import multiprocessing
import os
import pandas as pd
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from proto import bstream_pb2, bstream_pb2_grpc, codec_pb2
from requests_cache import CachedSession
from typing import Callable, Dict, List

load_dotenv(find_dotenv())

'''
	TODO
	====

	- Adapter pattern for processing block data (l84-l120)
	- Optimize asyncio workers => Have separate script for measuring the optimal parameters (?) -> How many blocks can I get from the gRPC connection at once ? Or is it one-by-one ?
	- Expand to other chains
	- Add opt-in integrity verification (using codec.Block variables)
	- More customisable data selection from traces (?)
	- Enable file format selection: Pandas/CSV, json/jsonl (?)
	- More argument parsing (?)
'''

def eos_block_processing(block: codec_pb2.Block) -> Dict:
	"""
	Yield a processed transaction from a block returning relevant properties.

	The signature of the function is crucial: it must take a `Block` object (properties defined in the `proto/codec.proto` file) and return a dict
	containing the desired properties for later storing in the `.jsonl` file. The basic template for processing transactions should look like this:
	```
		for transaction_trace in block.filtered_transaction_traces: # Gets every filtered TransactionTrace from the Block
			for action_trace in transaction_trace.action_traces: # Gets every ActionTrace within the TransactionTrace
				if not action_trace.filtering_matched: # Only keep 'transfer' actions that concerns the targeted accounts
					continue

				data = {}
				
				# Process the data...

				yield data
	```
	See `proto/codec.proto` file for a full list of available objects and properties.

	Args:
		block: The block to process transaction from.
	"""
	for transaction_trace in block.filtered_transaction_traces:
		for action_trace in transaction_trace.action_traces:
			logging.debug(f'[{asyncio.current_task().get_name()}] action_trace={action_trace}')
			
			if not action_trace.filtering_matched:
				continue

			action = action_trace.action
			try:
				json_data = json.loads(action.json_data)
			except Exception as e:
				logging.warning(f'Could not parse action (trxid={action_trace.transaction_id}): {e}\n')
				continue

			data = {
				'account': action_trace.receiver,
				'date': datetime.utcfromtimestamp(action_trace.block_time.seconds).strftime('%Y-%m-%d %H:%M:%S'),
				'amount': json_data['quantity'].split(' ')[0],
				'token': json_data['quantity'].split(' ')[1],
				'amountCAD': 0,
				'token/CAD': 0,
				'from': json_data['from'],
				'to': json_data['to'],
				'blockNum': transaction_trace.block_num,
				'trxID': action_trace.transaction_id,
				'memo': json_data['memo'],
				'contract': action.account,
				'action': action.name,
			}

			logging.debug(f'{data}')
			yield data

async def run(accounts: List[str], period_start: int, period_end: int, block_processor: Callable[[codec_pb2.Block], Dict], max_tasks: int = 20):
	"""
	Write a `.jsonl` file containing relevant transactions related to a list of accounts for a given period.

	It firsts obtains a JWT token from the `AUTH_ENDPOINT` defined in the `.env` file and uses this token to 
	authenticate with the Firehose gRPC service defined by `GRPC_ENDPOINT`. Then splits the block range into
	smaller ranges to process blocks in parallel using the `block_processor` function. Finally, it compiles
	all recorded transactions into a single `.jsonl` file in the `jsonl/` folder.

	Args:
		accounts: The accounts to look for as either recipient or sender of a transaction.
		period_start: The first block number of the targeted period.
		period_end: The last block number of the targeted period.
		block_processor: A generator function extracting relevant properties from a block. 
	"""
	async def stream_blocks(start: int, end: int) -> List[Dict]:
		"""
		Return a subset of transactions for blocks between `start` and `end` filtered by targeted accounts.

		Args:
			start: The Firehose stream's starting block 
			end: The Firehose stream's ending block

		Returns:
			A list of dictionaries describing the matching transactions. For example:
			[
				{
					'account': 'eosio.bpay',
					'date': 1665360012,
					'amount': '343.8791',
					'token': 'EOS',
					'amountCAD': 0,
					'token/CAD': 0,
					'from': 'eosio.bpay',
					'to': 'aus1genereos',
					'blockNum': 272368521,
					'trxID': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75',
					'memo': 'producer block pay',
					'contract': 'eosio.token',
					'action': 'transfer'
				},
				...
			]
		"""
		transactions = []
		
		logging.debug(f'[{asyncio.current_task().get_name()}] Starting streaming blocks from {start} to {end}...')
		async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
			start_block_num=start,
			stop_block_num=end,
			fork_steps=['STEP_IRREVERSIBLE'],
			include_filter_expr=f'receiver in {accounts} && action == "transfer"',
			exclude_filter_expr='action == "*"'
		)):
			b = codec_pb2.Block()
			response.block.Unpack(b) # Deserialize google.protobuf.Any to codec.Block

			logging.info(f'[{asyncio.current_task().get_name()}] Parsing block number #{b.number} ({end - b.number} blocks remaining)...')
			for t in block_processor(b):
				transactions.append(t)
		
		logging.info(f'[{asyncio.current_task().get_name()}] Done !\n')
		return transactions

	session = CachedSession(
		'jwt_token',
		expire_after=timedelta(days=1), # Cache JWT token (for up to 24 hours)
		allowable_methods=['GET', 'POST'],
	)

	headers = {'Content-Type': 'application/json',}
	data = f'{{"api_key":"{os.environ.get("DFUSE_TOKEN")}"}}'

	logging.info('Getting JWT token...')

	response = session.post(os.environ.get('AUTH_ENDPOINT'), headers=headers, data=data)
	if (response.status_code == 200):
		logging.debug(response.json())
		jwt = response.json()['token']
	else:
		logging.error(f'Could not load JWT token: {response.text}')
		exit(-1)

	logging.info(f'Got JWT token ({"cached" if response.from_cache else "new"}) [SUCCESS]')

	creds = grpc.composite_channel_credentials(grpc.ssl_channel_credentials(), grpc.access_token_call_credentials(jwt))
	block_diff = period_end - period_start
	max_tasks = block_diff if block_diff < max_tasks else max_tasks # Prevent having more tasks than block needing processing
	split = block_diff//max_tasks
	
	logging.info(f'Streaming {block_diff} blocks for transfer information related to {accounts} (running {max_tasks} concurrent tasks)...')
	console_handler.terminator = '\r'

	async with grpc.aio.secure_channel(os.environ.get('GRPC_ENDPOINT'), creds) as secure_channel:
		stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)
		tasks = []

		for i in range(max_tasks):
			tasks.append(
				asyncio.create_task(
					stream_blocks(
						period_start + i*split, 
						period_start + (i+1)*split if i < max_tasks-1 else period_end # Gives the remaining blocks to the last task in case the work can't be split equally
					)
				)
			)

		data = []
		for t in tasks:
			data += await t
		
	filename = f'jsonl/{"_".join(accounts)}_{period_start}_to_{period_end}.jsonl'
	with open(filename, 'w') as f:
		for entry in data:
			json.dump(entry, f)
			f.write('\n')
	
	console_handler.terminator = '\n'
	logging.info(f'Finished streaming, wrote {len(data)} rows of data to {filename} [SUCCESS]')

if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(
		description='Search the blockchain for transfer transactions targeting specific accounts over a given period. Powered by Firehose (https://eos.firehose.eosnation.io/).',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	arg_parser.add_argument('accounts', nargs='+', type=str, help='target account(s) (single or space-separated)')
	arg_parser.add_argument('block_start', type=int, help='starting block number')
	arg_parser.add_argument('block_end', type=int, help='ending block number')
	arg_parser.add_argument('--max-tasks', nargs='?', type=int, const=20, default=20, help='maximum number of concurrent tasks running for block streaming')
	arg_parser.add_argument('--debug', action='store_true', help='log debug information to log file (found in logs/)')
	arg_parser.add_argument('--no-log', action='store_true', help='disable console logging')

	args = arg_parser.parse_args()
	if args.block_end < args.block_start:
		arg_parser.error('block_start must be less than or equal to block_end')

	handlers = []
	if args.debug:
		handlers.append(logging.FileHandler('logs/' + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.log', mode='w')) # Unique log files

	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	handlers.append(console_handler)
	
	if args.no_log:
		logging.disable(logging.WARNING) # Keep only errors and critical messages

	logging.basicConfig(
		handlers=handlers,
		level=logging.DEBUG,
		format='T+%(relativeCreated)d\t%(levelname)s %(message)s',
		force=True
	)
	
	logging.addLevelName(logging.DEBUG, '[DEBUG]')
	logging.addLevelName(logging.INFO, '[*]')
	logging.addLevelName(logging.WARNING, '[!]')
	logging.addLevelName(logging.ERROR, '[ERROR]')
	logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

	asyncio.run(run(args.accounts, args.block_start, args.block_end, eos_block_processing, args.max_tasks))
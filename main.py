#!/usr/bin/env python3

import argparse
import asyncio
import grpc
import importlib
import inspect
import json
import logging
import os
import requests
import sys

from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from proto import bstream_pb2, bstream_pb2_grpc, codec_pb2
from requests_cache import CachedSession
from typing import Callable, Dict, List, Union

load_dotenv(find_dotenv())

'''
	TODO
	====

	- Optimize asyncio workers => Have separate script for measuring the optimal parameters (?) -> How many blocks can I get from the gRPC connection at once ? Or is it one-by-one ?
	- Error-checking for input arguments
	- Add opt-in integrity verification (using codec.Block variables)
	- Add more examples to README
	- Investigate functools and other more abstract modules for block processor modularity (?)
		- Possibility of 3 stages: pre-processing (e.g. load some API data), process (currently implemented), post-processing (e.g. adding more data to transactions)
'''

def parse_arguments() -> argparse.Namespace:
	"""
	Setup the command line interface and return the parsed arguments.

	Returns:
		A Namespace object containing the parsed arguments.
	"""
	arg_parser = argparse.ArgumentParser(
		description='Search the blockchain for transactions targeting specific accounts over a given period. Powered by Firehose (https://eos.firehose.eosnation.io/).',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	arg_parser.add_argument('accounts', nargs='+', type=str, help='target account(s) (single or space-separated)')
	arg_parser.add_argument('start', type=str, help='period start as a date (iso-like format) or a block number')
	arg_parser.add_argument('end', type=str, help='period end as a date (iso-like format) or a block number')
	arg_parser.add_argument('-c', '--chain', nargs=1, choices=['eos', 'wax', 'kylin', 'jungle4'], default='eos', help='target blockchain')
	arg_parser.add_argument('-n', '--max-tasks', nargs=1, type=int, default=20, help='maximum number of concurrent tasks running for block streaming')
	arg_parser.add_argument('-o', '--out-file', type=str, default='jsonl/{chain}_{accounts}_{start}_to_{end}.jsonl', help='output file path')
	arg_parser.add_argument('-l', '--log', nargs='?', type=str, const=None, default='logs/{datetime}.log', help='log debug information to log file (can specify the full path)')
	arg_parser.add_argument('-q', '--quiet', action='store_true', help='disable console logging')
	arg_parser.add_argument('-x', '--custom-exclude-expr', nargs=1, type=str, help='custom filter for the Firehose stream to exclude transactions')
	arg_parser.add_argument('-i', '--custom-include-expr', nargs=1, type=str, help='custom filter for the Firehose stream to tag included transactions')
	arg_parser.add_argument('-p', '--custom-processor', nargs=1, type=str, help='relative import path to a custom block processing function located in the "block_processors" module')
	arg_parser.add_argument('--disable-signature-check', action='store_true', help='disable signature checking for the custom block processing function')

	return arg_parser.parse_args()

def get_auth_token() -> str:
	"""
	Fetch a JWT authorization token from the AUTH_ENDPOINT defined in .env. Cache the token for 24-hour use.

	Returns:
		The JWT token or an empty string if the request failed.
	"""
	session = CachedSession(
		'jwt_token',
		expire_after=timedelta(days=1), # Cache JWT token (for up to 24 hours)
		allowable_methods=['GET', 'POST'],
	)

	headers = {'Content-Type': 'application/json',}
	data = f'{{"api_key":"{os.environ.get("DFUSE_TOKEN")}"}}'

	logging.info('Getting JWT token...')

	jwt = ''
	response = session.post(os.environ.get('AUTH_ENDPOINT'), headers=headers, data=data)
	
	if (response.status_code == 200):
		logging.debug(f'JWT response: {response.json()}')
		jwt = response.json()['token']
		logging.info(f'Got JWT token ({"cached" if response.from_cache else "new"}) [SUCCESS]')
	else:
		logging.error(f'Could not load JWT token: {response.text}') # TODO: Raise exception

	return jwt

def date_to_block_num(date: datetime, jwt: str = None) -> int:
	"""
	Queries the GraphQL API of the DFUSE_GRAPHQL_ENDPOINT specified in the .env file for the block number associated with a given date time.

	Args:
		date:
			A date to retrieve the associated block number.
		jwt:
			A JWT token used for authenticating with the GraphQL API (will be fetched automatically if not specified).

	Returns:
		The block number associated with the given date time.
	"""
	if not jwt:
		jwt = get_auth_token() # TODO: Catch exception

	headers = {'Authorization': f'Bearer {jwt}'}
	session = CachedSession(
		'graphql_rest',
		expire_after=timedelta(days=30),
		allowable_methods=['GET', 'POST'],
	)

	query = '''
	query ($date: Time!) {
		block: blockIDByTime(time: $date) {
			num
		}
	}
	'''

	variables = {
		'date': date.strftime('%Y-%m-%dT%H:%M:%SZ'),
	}

	data = {
		'query': query,
		'variables': variables
	}

	logging.info(f'Querying block number for {date}...')
	
	response = session.post(os.environ.get('DFUSE_GRAPHQL_ENDPOINT'), headers=headers, data=json.dumps(data))
	block_num = 0

	if response.status_code == 200:
		logging.debug(f'Block number query response: {response.json()}')
		block_num = response.json()['data']['block']['num']
		logging.info(f'Got response: block number #{block_num} [SUCCESS]')
	else:
		logging.warning(f'Could not fetch block number data ({response.status_code})') # TODO: Raise exception

	return block_num

async def run(accounts: List[str], period_start: Union[int, datetime], period_end: Union[int, datetime], block_processor: Callable[[codec_pb2.Block], Dict],
			  out_file: str, chain: str = 'eos', max_tasks: int = 20, custom_include_expr: str = None, custom_exclude_expr: str = None):
	"""
	Write a `.jsonl` file containing relevant transactions related to a list of accounts for a given period.

	It firsts obtains a JWT token from the `AUTH_ENDPOINT` defined in the `.env` file and uses this token to 
	authenticate with the Firehose gRPC service associated with the given chain. Then splits the block range 
	into smaller ranges to process blocks in parallel using the `block_processor` function. Finally, it 
	compiles all recorded transactions into a single `.jsonl` file in the `jsonl/` folder.

	Args:
		accounts:
			The accounts to look for as either recipient or sender of a transaction.
		period_start:
			The first block number or starting date of the targeted period.
		period_end:
			The last block number or ending date of the targeted period.
		block_processor:
			A generator function extracting relevant properties from a block.
		out_file:
			The path or filename for the output data file.
		chain:
			The target blockchain.
		max_tasks:
			The maximum number of concurrent tasks for streaming blocks.
		custom_include_expr:
			A custom Firehose filter for tagging blocks as included.
		custom_exclude_expr:
			A custom Firehose filter for excluding blocks from the results.
	"""
	async def stream_blocks(start: int, end: int) -> List[Dict]:
		"""
		Return a subset of transactions for blocks between `start` and `end` filtered by targeted accounts.

		Args:
			start:
				The Firehose stream's starting block 
			end:
				The Firehose stream's ending block

		Returns:
			A list of dictionaries describing the matching transactions. For example:
			[
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
				},
				...
			]
		"""
		transactions = []
		
		logging.debug(f'[{asyncio.current_task().get_name()}] Starting streaming blocks from {start} to {end} using "{block_processor.__name__}"...')
		async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
			start_block_num=start,
			stop_block_num=end,
			fork_steps=['STEP_IRREVERSIBLE'],
			include_filter_expr=custom_include_expr if custom_include_expr else f'receiver in {accounts} && action == "transfer"',
			exclude_filter_expr=custom_exclude_expr if custom_exclude_expr else 'action == "*"'
		)):
			b = codec_pb2.Block()
			response.block.Unpack(b) # Deserialize google.protobuf.Any to codec.Block

			logging.info(f'[{asyncio.current_task().get_name()}] Parsing block number #{b.number} ({end - b.number} blocks remaining)...')
			for t in block_processor(b): # TODO: Add exception handling
				transactions.append(t)
		
		logging.info(f'[{asyncio.current_task().get_name()}] Done !\n')
		return transactions

	jwt = get_auth_token()
	if not jwt:
		sys.exit(1)

	if isinstance(period_start, datetime):
		period_start = date_to_block_num(period_start, jwt)
	if isinstance(period_end, datetime):
		period_end = date_to_block_num(period_end, jwt)

	if not (period_start and period_end):
		logging.error(f'Invalid period: start={period_start}, end={period_end}')
		sys.exit(1)
	elif period_end < period_start:
		logging.error('period_start must be less than or equal to period_end')
		sys.exit(1)

	creds = grpc.composite_channel_credentials(grpc.ssl_channel_credentials(), grpc.access_token_call_credentials(jwt))
	block_diff = period_end - period_start
	max_tasks = block_diff if block_diff < max_tasks else max_tasks # Prevent having more tasks than the amount of blocks to process
	split = block_diff//max_tasks
	
	logging.info(f'Streaming {block_diff} blocks on {chain.upper()} chain for transfer information related to {accounts} (running {max_tasks} concurrent tasks)...')
	console_handler.terminator = '\r'

	async with grpc.aio.secure_channel(f'{chain}.firehose.eosnation.io:9000', creds) as secure_channel:
		stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)
		tasks = []

		for i in range(max_tasks):
			tasks.append(
				asyncio.create_task(
					stream_blocks(
						period_start + i*split, 
						period_start + (i+1)*split if i < max_tasks-1 else period_end # Gives the remaining blocks to the last task in case the work can't be splitted equally
					)
				)
			)

		data = []
		for t in tasks:
			data += await t
		
	with open(out_file, 'w') as f:
		for entry in data:
			json.dump(entry, f) # TODO: Add exception handling
			f.write('\n')
	
	console_handler.terminator = '\n'
	logging.info(f'Finished block streaming, wrote {len(data)} rows of data to {out_file} [SUCCESS]')

if __name__ == '__main__':
	args = parse_arguments()
	logging_handlers = []
	
	# === Arguments checking ===

	try:
		args.start = int(args.start)
	except ValueError:
		args.start = datetime.fromisoformat(args.start)

	try:
		args.end = int(args.end)
	except ValueError:
		args.end = datetime.fromisoformat(args.end)

	out_file = f'jsonl/{args.chain}_{"_".join(args.accounts)}_{args.start}_to_{args.end}.jsonl'
	if args.out_file != 'jsonl/{chain}_{accounts}_{start}_to_{end}.jsonl':
		out_file = args.out_file

	log_filename = 'logs/' + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
	if args.log != 'logs/{datetime}.log':
		if args.log:
			log_filename = args.log
		logging_handlers.append(logging.FileHandler(log_filename, mode='a+'))

	if args.quiet:
		logging.disable(logging.WARNING) # Keep only errors and critical messages
	
	module, function = ('block_processors.default', f'{args.chain}_block_processor')
	if args.custom_processor:
		module, function = args.custom_processor.rsplit('.', 1)
		module = f'block_processors.{module}'

	# === Logging setup ===

	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	logging_handlers.append(console_handler)
	
	logging.basicConfig(
		handlers=logging_handlers,
		level=logging.DEBUG,
		format='T+%(relativeCreated)d\t%(levelname)s %(message)s',
		force=True
	)
	
	logging.addLevelName(logging.DEBUG, '[DEBUG]')
	logging.addLevelName(logging.INFO, '[*]')
	logging.addLevelName(logging.WARNING, '[!]')
	logging.addLevelName(logging.ERROR, '[ERROR]')
	logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

	# === Block processor loading and startup ===

	try:
		block_processor = getattr(importlib.import_module(module), function)
		
		if not args.disable_signature_check:
			signature = inspect.signature(block_processor)
			parameters_annotations = [p_type.annotation for (_, p_type) in signature.parameters.items()]
			
			if (signature.return_annotation == signature.empty 
				or (not parameters_annotations and signature.parameters) # If there are parameters and none are annotated
				or any([t == inspect.Parameter.empty for t in parameters_annotations]) # If some parameters are not annotated
			):
				logging.warning('Could not check block processing function signature (make sure parameters and return value have type hinting annotations)')
			elif not codec_pb2.Block in parameters_annotations or signature.return_annotation != Dict or not inspect.isgeneratorfunction(block_processor):
				raise TypeError(f'Incompatible block processing function signature: {signature} should be <generator>(block: codec_pb2.Block) -> Dict')
	except Exception as e:
		logging.critical(f'Could not load block processing function: {e}')
		sys.exit(1)
	else:
		asyncio.run(
			run(
				accounts=args.accounts, 
				period_start=args.start, 
				period_end=args.end, 
				block_processor=block_processor,
				out_file=out_file,
				chain=args.chain, 
				max_tasks=args.max_tasks,
				custom_include_expr=args.custom_include_expr,
				custom_exclude_expr=args.custom_exclude_expr,
			)
		)